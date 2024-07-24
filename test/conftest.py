#!/usr/bin/env python

import os
import django
import pytest

from django.conf import settings

# We manually designate which settings we will be using in an environment
# variable. This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omeroweb.settings')


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = False
    settings.SERVER_ADDRESS = '"http://localhost:4080"'
    settings.django.setup()
