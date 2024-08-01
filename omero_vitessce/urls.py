from django.urls import re_path

from . import views

urlpatterns = [
    # Generate config Button
    re_path(r"^generate_config/(?P<obj_type>[a-z]+)/(?P<obj_id>[0-9]+)",
            views.generate_config, name='generate_config'),

    # Button placeholder
    re_path(r"^generate_config$", views.vitessce_index,
            name="generate_config"),

    # Right panel plugin
    re_path(r"(?P<obj_type>[a-z]+)/(?P<obj_id>[0-9]+)",
            views.vitessce_panel, name='vitessce_tab'),

    # Index placeholder for right panel plugin
    re_path(r"^$", views.vitessce_index, name="vitessce_tab"),

    # Open-with
    re_path(r"^open/",
            views.vitessce_open, name='open_vitessce')

]
