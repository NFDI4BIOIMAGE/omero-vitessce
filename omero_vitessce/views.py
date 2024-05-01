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


# login_required: if not logged-in, will redirect to webclient
# login page. Then back to here, passing in the 'conn' connection
# and other arguments **kwargs.
@login_required()
def vitessce_panel(request, conn=None, **kwargs):

    # Get all .json attachements and generate links for them
    config_files = conn.getObjects("FileAnnotation")
    config_files = ["AAAAA", "BBBBB"] 
    
    context = {"json_configs": config_files}

    # Render the html template and return the http response
    return render(request, "omero_vitessce/vitessce_panel.html", context)
