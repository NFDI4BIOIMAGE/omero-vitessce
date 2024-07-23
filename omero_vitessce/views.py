#
# Copyright (c) 2017 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.shortcuts import render

from omeroweb.decorators import login_required

from . import omero_vitessce_settings


# Get the address of omeroweb from the config
SERVER = omero_vitessce_settings.SERVER_ADDRESS[1:-1]


# login_required: if not logged-in, will redirect to webclient
# login page. Then back to here, passing in the 'conn' connection
# and other arguments **kwargs.
@login_required()
def vitessce_index(request, conn=None, **kwargs):
    # Render the html template and return the http response
    return render(request, "omero_vitessce/index.html")

@login_required()
def vitessce_panel(request, obj_type, obj_id, conn=None, **kwargs):

    # Generate an openlink space

    # Get all .json.txt attachements and generate links for them
    # This way the config files can be served as text to the config argument of the vitessce webapp
    obj_id = int(obj_id)
    obj = conn.getObject(obj_type, obj_id)
    config_files = [i for i in obj.listAnnotations() if i.OMERO_TYPE().NAME == "ome.model.annotations.FileAnnotation_name"]
    config_urls = [str(i.getId()) for i in config_files if i.getFileName().endswith(".json.txt")]
    config_files = [i.getFileName() for i in config_files if i.getFileName().endswith(".json.txt")]
    config_urls = [SERVER + "/omero_vitessce/?config=" + SERVER + "/webclient/annotation/" + i for i in config_urls]

    context = {"json_configs": dict(zip(config_files, config_urls)), "obj_type" : obj_type, "obj_id" : obj_id}

    # Render the html template and return the http response
    return render(request, "omero_vitessce/vitessce_panel.html", context)

