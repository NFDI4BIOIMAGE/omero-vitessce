"""Integration tests for index page."""
import pytest

import omero.model
from omero.rtypes import rstring, rdouble
from omeroweb.testlib import IWebTest
from omero.gateway import BlitzGateway

from omero_vitessce import utils


def add_roi_polygon(img, points, name, conn):
    polygon = omero.model.PolygonI()
    polygon.points = rstring(points)
    polygon.setTextValue(rstring(name))
    roi = omero.model.RoiI()
    roi.addShape(polygon)
    roi.setImage(img._obj)
    roi = conn.getUpdateService().saveAndReturnObject(roi)
    return roi.getId().getValue()


def add_roi_rectangle(img, x, y, w, h, name, conn):
    rect = omero.model.RectangleI()
    rect.setX(rdouble(x))
    rect.setY(rdouble(y))
    rect.setWidth(rdouble(w))
    rect.setHeight(rdouble(h))
    rect.setTextValue(rstring(name))
    roi = omero.model.RoiI()
    roi.addShape(rect)
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
        rois.append(
            add_roi_polygon(img, "10,20, 200,200, 250,75 300,250, 75,400",
                            "A", conn))
        rois.append(add_roi_polygon(img, "10,20, 50,150, 250,75", "B", conn))
        img = conn.getObject("Image", 2)
        rois.append(add_roi_rectangle(img, 0, 0, 10, 5, "C", conn))
        rois.append(add_roi_rectangle(img, 3333, 6666, 1000, 2000, "D", conn))
        yield rois
        conn.deleteObjects("Roi", rois)

    def test_rois(self, conn, rois):
        shapes = utils.process_rois([1, 2], conn)
        obs_dict = utils.make_cell_json(shapes)  # OMERO uses floats
        exp_dict = {"A": [(10.0, 20.0), (200.0, 200.0),
                          (250.0, 75.0), (300.0, 250.0),
                          (75.0, 400.0), (10.0, 20.0)],
                    "B": [(10.0, 20.0), (50.0, 150.0),
                          (250.0, 75.0), (10.0, 20.0)],
                    "C": [(0.0, 0.0), (10.0, 0.0),
                          (10.0, 5.0), (0.0, 5.0), (0.0, 0.0)],
                    "D": [(3333.0, 6666.0), (4333.0, 6666.0),
                          (4333.0, 8666.0), (3333.0, 8666.0),
                          (3333.0, 6666.0)]}
        assert obs_dict == exp_dict
