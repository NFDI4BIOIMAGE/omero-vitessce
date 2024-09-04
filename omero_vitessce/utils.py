import json
from pathlib import Path

from omero.util.temp_files import create_path

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
    for the files and eventually the images.
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
    file_urls = [SERVER + "/webclient/annotation/" + str(i) for i in file_urls]

    if obj_type == "dataset":
        imgs = list(obj.listChildren())
        img_urls = [build_zarr_image_url(i.getId()) for i in imgs]
        img_names = [i.getName() for i in imgs]
    else:
        img_urls = [build_zarr_image_url(obj_id)]
        img_names = [obj.getName()]

    return file_names, file_urls, img_names, img_urls


def build_viewer_url(config_id):
    """ Generates urls like:
    http://localhost:4080/omero_vitessce/?config=http://localhost:4080/webclient/annotation/999
    """
    return SERVER + "/omero_vitessce/?config=" + SERVER + \
        "/webclient/annotation/" + str(config_id)


def build_zarr_image_url(image_id):
    """ Generates urls like:
    http://localhost:4080/zarr/v0.4/image/99999.zarr/
    """
    return SERVER + "/zarr/v0.4/image/" + str(image_id) + ".zarr"


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


def create_config(config_args, obj_type, obj_id, conn):
    """
    Generates a Vitessce config and returns it,
    the results from the form are used as args.
    """

    description, name = get_details(obj_type, obj_id, conn)

    vc = VitessceConfig(schema_version="1.0.16",
                        name=name, description=description)
    vc_dataset = vc.add_dataset()

    img_url = config_args.get("image")
    images = [OmeZarrWrapper(img_url=img_url, name="Image")]

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
        Ct.SPATIAL_TARGET_Y: 0
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

    return vc


def attach_config(vc, obj_type, obj_id, filename, conn):
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
        json.dump(vc.to_dict(), outfile, indent=4, sort_keys=False)

    file_ann = conn.createFileAnnfromLocalFile(
        config_path, mimetype="text/plain")
    obj = conn.getObject(obj_type, obj_id)
    obj.linkAnnotation(file_ann)
    return file_ann.getId()
