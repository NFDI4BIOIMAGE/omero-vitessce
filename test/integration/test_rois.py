"""Integration tests for index page."""
import pytest

import omero.model
from omero.rtypes import rstring
from omeroweb.testlib import IWebTest
from omero.gateway import BlitzGateway

from omero_vitessce import utils


def add_roi(img, points, name, conn):
    polygon = omero.model.PolygonI()
    polygon.points = rstring(points)
    polygon.setTextValue(rstring(name))
    roi = omero.model.RoiI()
    roi.addShape(polygon)
    roi.setImage(img._obj)
    roi = conn.getUpdateService().saveAndReturnObject(roi)
    return roi.getId().getValue()


class TestConfig(IWebTest):
    """Tests loading the index page."""
    USER_NAME = "test_user"
    USER_GROUP = "TestGroup"
    USER_PWD = "password"

    @pytest.fixture()
    def conn(self):
        """Set up a connection to the user/group holding the test data"""
        client = IWebTest.new_client(self, group=TestConfig.USER_GROUP,
                                     user=TestConfig.USER_NAME, perms=None,
                                     owner=False, system=False, session=None,
                                     password=TestConfig.USER_PWD, email=None,
                                     privileges=None)
        conn = BlitzGateway(client_obj=client)
        return conn

    @pytest.fixture()
    def rois(self, conn):
        """make two mock ROIs and link them to Image:1 and Image:2"""
        rois = []
        img = conn.getObject("Image", 1)
        rois.append(add_roi(img, "10,20, 50,150, 200,200, 250,75", "A", conn))
        img = conn.getObject("Image", 2)
        rois.append(add_roi(img, "10,20, 50,150, 250,75", "B", conn))
        yield rois
        conn.deleteObjects("Roi", rois)

    def test_rois(self, conn, rois):
        shapes = utils.process_rois([1, 2], conn)
        obs_dict = utils.make_cell_json(shapes)  # We get floats from OMERO
        exp_dict = {"A": [(10.0, 20.0), (50.0, 150.0),
                          (200.0, 200.0), (250.0, 75.0), (10.0, 20.0)],
                    "B": [(10.0, 20.0), (50.0, 150.0),
                          (250.0, 75.0), (10.0, 20.0)]}
        assert obs_dict == exp_dict
