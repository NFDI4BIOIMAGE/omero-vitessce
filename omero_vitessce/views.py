import tempfile
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect

from omeroweb.webclient.decorators import login_required

from . import omero_vitessce_settings

from vitessce import VitessceConfig
from vitessce import ViewType as vt, FileType as ft, CoordinationType as ct

# Get the address of omeroweb from the config
SERVER = omero_vitessce_settings.SERVER_ADDRESS[1:-1]


def build_viewer_url(config_id):
    return SERVER + "/omero_vitessce/?config=" + SERVER + \
            "/webclient/annotation/" + str(config_id)


def get_attached_configs(obj_type, obj_id, conn):
    obj = conn.getObject(obj_type, obj_id)
    config_files = [i for i in obj.listAnnotations()
                    if i.OMERO_TYPE().NAME ==
                    "ome.model.annotations.FileAnnotation_name"]
    config_urls = [i.getId() for i in config_files
                   if i.getFileName().endswith(".json.txt")]
    config_files = [i.getFileName() for i in config_files
                    if i.getFileName().endswith(".json.txt")]
    config_urls = [build_viewer_url(i) for i in config_urls]
    return config_files, config_urls


def create_dataset_config(dataset_id):
    # TO DO
    pass


def create_image_config(image_id):
    vc = VitessceConfig(schema_version="1.0.6")
    vc_dataset = vc.add_dataset().add_file(
            url=SERVER + "/zarr/v0.4/image/" + str(image_id) + ".zarr",
            file_type=ft.IMAGE_OME_ZARR)
    vc.add_view(vt.SPATIAL, dataset=vc_dataset, x=0, y=0, w=10, h=10)
    vc.add_view(vt.LAYER_CONTROLLER, dataset=vc_dataset, x=10, y=0, w=2, h=10)
    vc.add_coordination_by_dict({
        ct.SPATIAL_ZOOM: 2,
        ct.SPATIAL_TARGET_X: 0,
        ct.SPATIAL_TARGET_Y: 0,
    })
    return vc


def attach_config(vc, obj_id, obj_type, conn):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json.txt",
                                     delete=False) as outfile:
        json.dump(vc.to_dict(), outfile, indent=4, sort_keys=False)
    file_ann = conn.createFileAnnfromLocalFile(
                outfile.name, mimetype="text/plain")
    obj = conn.getObject(obj_type, obj_id)
    obj.linkAnnotation(file_ann)
    return file_ann.getId()


@login_required()
def vitessce_index(request, conn=None, **kwargs):
    # Render the basic index page for the app
    return render(request, "omero_vitessce/index.html")


@login_required()
def vitessce_panel(request, obj_type, obj_id, conn=None, **kwargs):
    # Get all .json.txt attachements and generate links for them
    # This way the config files can be served as text
    # to the config argument of the vitessce webapp
    obj_id = int(obj_id)

    config_files, config_urls = get_attached_configs(obj_type, obj_id, conn)

    context = {"json_configs": dict(zip(config_files, config_urls)),
               "obj_type": obj_type, "obj_id": obj_id}

    return render(request, "omero_vitessce/vitessce_panel.html", context)


@login_required(setGroupContext=True)
def generate_config(request, obj_type, obj_id, conn=None, **kwargs):
    # Get all .json.txt attachements and generate links for them
    # This way the config files can be served as text
    # to the config argument of the vitessce webapp

    obj_id = int(obj_id)
    if obj_type == "image":
        vitessce_config = create_image_config(obj_id)
    if obj_type == "dataset":
        vitessce_config = create_dataset_config(obj_id)

    # config_id=attach_config(vitessce_config, obj_type, obj_id, conn)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json.txt",
                                     delete=False) as outfile:
        json.dump(vitessce_config.to_dict(),
                  outfile, indent=4, sort_keys=False)
    file_ann = conn.createFileAnnfromLocalFile(
                outfile.name, mimetype="text/plain")
    obj = conn.getObject(obj_type, obj_id)
    obj.linkAnnotation(file_ann)
    config_id = file_ann.getId()

    viewer_url = build_viewer_url(config_id)

    return HttpResponseRedirect(viewer_url)


@login_required()
def vitessce_open(request, conn=None, **kwargs):
    # Get the first .json.txt attachement and generate a link for it
    # This way the config files can be served as text
    # If no config files are present send to the panel html to ask to make one
    if request.GET.get("project") is not None:
        obj_type = "project"
        obj_id = int(request.GET.get("project"))
    elif request.GET.get("dataset") is not None:
        obj_type = "dataset"
        obj_id = int(request.GET.get("dataset"))
    elif request.GET.get("image") is not None:
        obj_type = "image"
        obj_id = int(request.GET.get("image"))
    else:
        context = {"json_configs": dict(),
                   "obj_type": obj_type, "obj_id": obj_id}
        return render(request, "omero_vitessce/vitessce_panel.html", context)

    _, config_urls = get_attached_configs(obj_type, obj_id, conn)

    if len(config_urls) > 0:
        return HttpResponseRedirect(config_urls[0])
    else:
        context = {"json_configs": dict(),
                   "obj_type": obj_type, "obj_id": obj_id}
        return render(request, "omero_vitessce/vitessce_panel.html", context)
