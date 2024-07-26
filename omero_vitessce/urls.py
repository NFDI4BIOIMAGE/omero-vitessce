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

from django.urls import re_path

from . import views

urlpatterns = [
    # Right panel plugin
    re_path(r"(?P<obj_type>[a-z]+)/(?P<obj_id>[0-9]+)",
            views.vitessce_panel, name='vitessce_tab'),

    # Index placeholder for right panel plugin
    re_path(r"^$", views.vitessce_index, name="vitessce_tab"),

    # Open-with
    re_path(r"^open/",
            views.vitessce_open, name='open_vitessce')

]
