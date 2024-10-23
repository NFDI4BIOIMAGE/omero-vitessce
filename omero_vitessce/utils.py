import json
from pathlib import Path
from shapely.geometry import Polygon
from omero_marshal import get_encoder

from omero.util.temp_files import create_path

from .forms import ConfigForm
from . import omero_vitessce_settings

from vitessce import VitessceConfig, OmeZarrWrapper, MultiImageWrapper
from vitessce import ViewType as Vt, FileType as Ft, CoordinationType as Ct
from vitessce import hconcat, vconcat

# Get the address of omeroweb from the config
SERVER = omero_vitessce_settings.SERVER_ADDRESS[1:-1]


def get_files_images(obj_type, obj_id, conn):
    """ Gets all the non config files attached to an object,
    and images if the object is a dataset,
    and returns a list of file names and a list of urls
    for the files and eventually the images, plus the image ids.
    """
    obj = conn.getObject(obj_type, obj_id)
    file_names = [
            i for i in obj.listAnnotations()
            if i.OMERO_TYPE().NAME ==
            "ome.model.annotations.FileAnnotation_name"]
    file_names = [i for i in file_names
                  if i.getFileName().endswith(".csv")]
    file_urls = [i.getId() for i in file_names]
    file_names = [i.getFileName() for i in file_names]
    file_urls = [build_attachement_url(i) for i in file_urls]

    if obj_type == "dataset":
        imgs = list(obj.listChildren())
        img_ids = [i.getId() for i in imgs]
        img_urls = [build_zarr_image_url(i) for i in img_ids]
        img_names = [i.getName() for i in imgs]
    else:
        img_urls = [build_zarr_image_url(obj_id)]
        img_names = [obj.getName()]
        img_ids = [obj_id]

    return file_names, file_urls, img_names, img_urls, img_ids


def build_viewer_url(config_id):
    """ Generates urls like:
    http://localhost:4080/omero_vitessce/?config=http://localhost:4080/webclient/annotation/999
    """
    return SERVER + "/omero_vitessce/?config=" + SERVER + \
        "/webclient/annotation/" + str(config_id)


def build_zarr_image_url(image_id):
    """ Generates urls like:
    http://localhost:4080/zarr/v0.4/image/99999.zarr
    """
    return SERVER + "/zarr/v0.4/image/" + str(image_id) + ".zarr"


def build_attachement_url(obj_id):
    """ Generates urls like:
    http://localhost:4080/webclient/annotation/99999
    """
    return SERVER + "/webclient/annotation/" + str(obj_id)


def get_attached_configs(obj_type, obj_id, conn):
    """ Gets all the ".json" files attached to an object
    and returns a list of file names and a list of urls
    generated with build_viewer_url
    """
    obj = conn.getObject(obj_type, obj_id)
    config_files = [i for i in obj.listAnnotations()
                    if i.OMERO_TYPE().NAME ==
                    "ome.model.annotations.FileAnnotation_name"]
    config_urls = [i.getId() for i in config_files
                   if i.getFileName().endswith(".json")]
    config_files = [i.getFileName() for i in config_files
                    if i.getFileName().endswith(".json")]
    config_urls = [build_viewer_url(i) for i in config_urls]
    return config_files, config_urls


def get_details(obj_type, obj_id, conn):
    """ Gets all the ".json" files attached to an object
    and returns a list of file names and a list of urls
    generated with build_viewer_url
    """
    obj = conn.getObject(obj_type, obj_id)
    name = obj.getName()
    description = obj.getDescription()
    if not description:
        description = "Generated with omero-vitessce"
    return description, name


def add_molecules(config_args, vc_dataset):
    """
    Adds a file with molecule labels and locations to a vitessce dataset
    """
    vc_dataset = vc_dataset.add_file(
        url=config_args.get("molecules"),
        file_type=Ft.OBS_LOCATIONS_CSV,
        coordination_values={
            "obsType": "molecule"},
        options={
            "obsIndex": config_args.get("molecule_id"),
            "obsLocations": [config_args.get("molecule_x"),
                             config_args.get("molecule_y")]})
    vc_dataset = vc_dataset.add_file(
        url=config_args.get("molecules"),
        file_type=Ft.OBS_LABELS_CSV,
        coordination_values={
            "obsType": "molecule"},
        options={
            "obsIndex": config_args.get("molecule_id"),
            "obsLabels": config_args.get("molecule_label")})
    return vc_dataset


def add_embeddings(config_args, vc_dataset):
    """
    Adds a file with cell embeddings to a vitessce dataset
    """
    vc_dataset = vc_dataset.add_file(
        url=config_args.get("embeddings"),
        file_type=Ft.OBS_EMBEDDING_CSV,
        coordination_values={
            "obsType": "cell",
            "embeddingType": "cell"},
        options={
            "obsIndex": config_args.get("cell_id_column"),
            "obsEmbedding": [config_args.get("embedding_x"),
                             config_args.get("embedding_y")]})
    return vc_dataset


def add_cell_identities(config_args, vc_dataset):
    """
    Adds a file with cell identities to a vitessce dataset
    """
    vc_dataset = vc_dataset.add_file(
        url=config_args.get("cell_identities"),
        file_type=Ft.OBS_SETS_CSV,
        coordination_values={"obsType": "cell"},
        options={
            "obsIndex": config_args.get("cell_id_column"),
            "obsSets": [
                {"name": "Clustering",
                 "column": config_args.get("cell_label_column")}]})
    return vc_dataset


class VitessceShape():
    """
    Converts an OMERO ROI shape to a vitessce compatibel represetnation
    https://github.com/will-moore/omero-vitessce/blob/master/omero_vitessce/views.py
    """
    def __init__(self, shape):
        self.shape = self.to_shapely(shape)
        self.name = shape.getTextValue().getValue()

    def to_shapely(self, omero_shape):
        encoder = get_encoder(omero_shape.__class__)
        shape_json = encoder.encode(omero_shape)

        if "Points" in shape_json:
            xy = shape_json["Points"].split(" ")
            coords = []
            for coord in xy:
                c = coord.split(",")
                coords.append((float(c[0]), float(c[1])))
            return Polygon(coords)

    def poly(self):
        # Use 2 to get e.g. 8 points from 56.
        return list(self.shape.simplify(2).exterior.coords)


def process_rois(img_ids, conn):
    """
    Generates shapely polygons from OMERO rois,
    extracted from a list of images
    """
    rois = []
    for img_id in img_ids:
        img = conn.getObject("Image", img_id)
        if not img:
            continue
        rois += img.getROIs()
    shapes = [VitessceShape(r.getShape(0)) for r in rois]
    return shapes


def make_cell_json(shapes):
    """
    Turns a list of polygons into a dictionary:
    {cell_id: [[x, y], ...]}
    """
    cell_dict = {}
    for s in shapes:
        cell_dict[s.name] = s.poly()
    return cell_dict


def add_rois(img_ids, vc_dataset, conn):
    """
    Adds a url to the rois in json format to the vitessce config
    """
    cell_json_url = SERVER + "/omero_vitessce/vitessce_json_rois/" + \
        ",".join([str(i) for i in img_ids])
    vc_dataset = vc_dataset.add_file(
        url=cell_json_url,
        file_type=Ft.OBS_SEGMENTATIONS_JSON,
        coordination_values={"obsType": "cell"})
    return vc_dataset


def create_config(config_args, obj_type, obj_id, conn):
    """
    Generates a Vitessce config and returns it,
    the results from the form are used as args.
    """

    # If an attachment/image is deleted/moved between the Vitessce right tab
    # plugin is loaded and the form is submitted then it will not be found
    # and will not be present in the cleaned_data -> None

    file_names, file_urls, img_files, img_urls, img_ids = get_files_images(
        obj_type, obj_id, conn)
    config_args = ConfigForm(data=config_args, file_names=file_names,
                             file_urls=file_urls, img_names=img_files,
                             img_urls=img_urls)
    config_args.is_valid()  # Generates the cleaned data
    config_args = config_args.cleaned_data
    description, name = get_details(obj_type, obj_id, conn)

    vc = VitessceConfig(schema_version="1.0.16",
                        name=name, description=description)
    vc_dataset = vc.add_dataset()

    images = []
    img_urls = config_args.get("images")
    for n, img_url in enumerate(img_urls):
        images.append(OmeZarrWrapper(img_url=img_url, name=f"Image {n}"))

    sp = vc.add_view(Vt.SPATIAL, dataset=vc_dataset)
    lc = vc.add_view(Vt.LAYER_CONTROLLER, dataset=vc_dataset)

    displays = [sp]     # Heatmap, scatterplot and image
    controllers = [lc]  # Spatial layer, gene and cell set selectors
    hists = []          # Histograms and violin plots
    texts = []          # Status and description

    if config_args.get("cell_identities"):
        vc_dataset = add_cell_identities(config_args, vc_dataset)
        os = vc.add_view(Vt.OBS_SETS, dataset=vc_dataset)
        controllers.append(os)
    if config_args.get("expression"):
        vc_dataset = vc_dataset.add_file(
            url=config_args.get("expression"),
            file_type=Ft.OBS_FEATURE_MATRIX_CSV)
        fl = vc.add_view(Vt.FEATURE_LIST, dataset=vc_dataset)
        controllers.append(fl)
    if config_args.get("embeddings"):
        vc_dataset = add_embeddings(config_args, vc_dataset)
        e_type = vc.add_coordination(Ct.EMBEDDING_TYPE)[0]
        e_type.set_value("cell")
        sc = vc.add_view(Vt.SCATTERPLOT, dataset=vc_dataset)
        sc.use_coordination(e_type)
        displays.append(sc)
    if config_args.get("expression") and config_args.get("cell_identities"):
        if config_args.get("histograms"):
            fh = vc.add_view(Vt.FEATURE_VALUE_HISTOGRAM, dataset=vc_dataset)
            oh = vc.add_view(Vt.OBS_SET_SIZES, dataset=vc_dataset)
            fd = vc.add_view(Vt.OBS_SET_FEATURE_VALUE_DISTRIBUTION,
                             dataset=vc_dataset)
            hists.extend([fh, oh, fd])
        if config_args.get("heatmap"):
            hm = vc.add_view(Vt.HEATMAP, dataset=vc_dataset)
            displays.append(hm)
    if config_args.get("segmentation"):
        segmentation = OmeZarrWrapper(
                img_url=config_args.get("segmentation"),
                name="Segmentation", is_bitmask=True)
        images.append(segmentation)
    if config_args.get("rois"):
        vc_dataset = add_rois(img_ids, vc_dataset, conn)
        vc.link_views([sp, lc], ["spatialSegmentationLayer"],
                      [{"opacity": 1, "radius": 0,
                        "visible": True, "stroked": False}])
    if config_args.get("molecules"):
        vc_dataset = add_molecules(config_args, vc_dataset)
        vc.link_views([sp, lc], c_types=[Ct.SPATIAL_POINT_LAYER],
                      c_values=[{"opacity": 1, "radius": 2, "visible": True}])
    if config_args.get("description"):
        de = vc.add_view(Vt.DESCRIPTION, dataset=vc_dataset)
        texts.append(de)
    if config_args.get("status"):
        st = vc.add_view(Vt.STATUS, dataset=vc_dataset)
        texts.append(st)

    vc_dataset.add_object(MultiImageWrapper(image_wrappers=images,
                                            use_physical_size_scaling=True))
    vc.add_coordination_by_dict({
        Ct.SPATIAL_ZOOM: 2,
        Ct.SPATIAL_TARGET_X: 0,
        Ct.SPATIAL_TARGET_Y: 0,
    })

    displays = hconcat(*displays)
    controllers = hconcat(*controllers)
    if texts:
        texts = vconcat(*texts)
        controllers = hconcat(texts, controllers)
    if hists:
        hists = hconcat(*hists)
        controllers = hconcat(controllers, hists)
    vc.layout(vconcat(displays, controllers))

    vc_dict = vc.to_dict()

    # OBS_SEGMENTATIONS_JSON does not work with raster.json
    # https://github.com/vitessce/vitessce/discussions/1962
    if config_args.get("rois"):
        for d in vc_dict["datasets"]:
            for f in d["files"]:
                if f["fileType"] == "raster.json":
                    f["fileType"] = "image.raster.json"

    return vc_dict


def attach_config(vc_dict, obj_type, obj_id, filename, conn):
    """
    Generates a Vitessce config for an OMERO image and returns it.
    Assumes the images is an OME NGFF v0.4 file
    which can be served with omero-web-zarr.
    """
    config_path = create_path("omero-vitessce", ".tmp", folder=True)
    if not filename.endswith(".json"):
        filename = filename + ".json"
    filename = Path(filename).name  # Sanitize filename

    config_path = Path(config_path).joinpath(filename)
    with open(config_path, "w") as outfile:
        json.dump(vc_dict, outfile, indent=4, sort_keys=False)

    file_ann = conn.createFileAnnfromLocalFile(
        config_path, mimetype="text/plain")
    obj = conn.getObject(obj_type, obj_id)
    obj.linkAnnotation(file_ann)
    return file_ann.getId()
