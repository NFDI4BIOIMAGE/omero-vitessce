from django.shortcuts import render
from django.http import HttpResponseRedirect

from omeroweb.decorators import login_required

from . import omero_vitessce_settings

from vitessce import VitessceConfig, ViewType as vt, FileType as ft, CoordinationType as ct

# Get the address of omeroweb from the config
SERVER = omero_vitessce_settings.SERVER_ADDRESS[1:-1]

def get_attached_configs(obj_type, obj_id, conn):
    obj = conn.getObject(obj_type, obj_id)
    config_files = [i for i in obj.listAnnotations()
                    if i.OMERO_TYPE().NAME ==
                    "ome.model.annotations.FileAnnotation_name"]
    config_urls = [str(i.getId()) for i in config_files
                   if i.getFileName().endswith(".json.txt")]
    config_files = [i.getFileName() for i in config_files
                    if i.getFileName().endswith(".json.txt")]
    config_urls = [SERVER + "/omero_vitessce/?config=" + SERVER
                   + "/webclient/annotation/" + i for i in config_urls]
    return config_files, config_urls


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

    # Render the html template and return the http response
    return render(request, "omero_vitessce/vitessce_panel.html", context)


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
