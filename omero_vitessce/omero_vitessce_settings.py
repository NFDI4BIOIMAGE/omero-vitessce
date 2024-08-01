import sys
from omeroweb.settings import process_custom_settings, report_settings


def str_not_empty(o):
    """Checks for empty/invalid strings.
    """
    s = str(o)
    if not o or not s:
        raise ValueError('Invalid empty value')
    return s


OMEROVITESSCE_SETTINGS_MAPPINGS = {
    'omero.web.omero_vitessce.serveraddress': ['SERVER_ADDRESS',
                                               '"http://localhost:4080"',
                                               str_not_empty, None]
}

process_custom_settings(sys.modules[__name__],
                        'OMEROVITESSCE_SETTINGS_MAPPINGS')
report_settings(sys.modules[__name__])
