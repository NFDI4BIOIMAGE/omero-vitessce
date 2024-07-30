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
