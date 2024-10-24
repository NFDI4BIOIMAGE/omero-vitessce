"""Integration tests for index page."""
import json
import os
import pytest

from omeroweb.testlib import IWebTest
from django.http.request import HttpRequest
from django.http.request import QueryDict
from omero.gateway import BlitzGateway

from omero_vitessce import utils


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

    def test_image_files(self, conn):
        """Checks the retrieval of images and .csv attachements"""
        i1_e = (set([]), set([]), set(["MB266-DAPI.tiff"]),
                set(["http://localhost:4080/zarr/v0.4/image/1.zarr"]),
                set([1]))
        i2_e = (set([]), set([]), set(["MB266-CELLS.png"]),
                set(["http://localhost:4080/zarr/v0.4/image/2.zarr"]),
                set([2]))
        d1_e = (set(["cells.csv", "embeddings.csv", "transcripts.csv",
                     "feature_matrix.csv"]),
                set(["http://localhost:4080/webclient/annotation/1",
                     "http://localhost:4080/webclient/annotation/2",
                     "http://localhost:4080/webclient/annotation/3",
                     "http://localhost:4080/webclient/annotation/4"]),
                set(["MB266-DAPI.tiff", "MB266-CELLS.png"]),
                set(["http://localhost:4080/zarr/v0.4/image/1.zarr",
                     "http://localhost:4080/zarr/v0.4/image/2.zarr"]),
                set([1, 2]))

        i1_o = tuple(set(i) for i in utils.get_files_images("image", 1, conn))
        i2_o = tuple(set(i) for i in utils.get_files_images("image", 2, conn))
        d1_o = tuple(set(i) for i in utils.get_files_images("dataset",
                                                            1, conn))

        errors = []
        if i1_o != i1_e:
            errors.append(
                    f"Wrong files found on image 1 {i1_o}, should be {i1_e}")
        if i2_o != i2_e:
            errors.append(
                    f"Wrong files found on image 2 {i2_o}, should be {i2_e}")
        if d1_o != d1_e:
            errors.append(
                    f"Wrong files found on dataset 1 {d1_o}, should be {d1_e}")
        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    def test_config_files(self, conn):
        """Checks the retrieval of .json config files"""
        i1_e = (set([]), set([]))
        i2_e = (set([]), set([]))
        d1_e = (set(["VitessceConfig.json"]), set([
            "http://localhost:4080/omero_vitessce/" +
            "?config=http://localhost:4080/webclient/annotation/5"
            ]))

        i1_o = tuple(set(i) for i in utils.get_attached_configs("image",
                                                                1, conn))
        i2_o = tuple(set(i) for i in utils.get_attached_configs("image",
                                                                2, conn))
        d1_o = tuple(set(i) for i in utils.get_attached_configs("dataset",
                                                                1, conn))

        errors = []
        if i1_o != i1_e:
            errors.append(
                    f"Wrong files found on image 1 {i1_o}, should be {i1_e}")
        if i2_o != i2_e:
            errors.append(
                    f"Wrong files found on image 2 {i2_o}, should be {i2_e}")
        if d1_o != d1_e:
            errors.append(
                    f"Wrong files found on dataset 1 {d1_o}, should be {d1_e}")
        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    def test_config_file(self, conn):
        """Test loading the app home page."""
        json_path = os.path.join(os.environ["TARGET"],
                                 "test/data/MB266/VitessceConfig.json")
        with open(json_path) as jf:
            expected_json = json.load(jf)
        config_data = HttpRequest()
        text = ("config_file_name=VitessceConfig.json&"
                "images="
                "http%3A%2F%2Flocalhost%3A4080%2F"
                "zarr%2Fv0.4%2Fimage%2F1.zarr&"
                "segmentation="
                "http%3A%2F%2Flocalhost%3A4080%2F"
                "zarr%2Fv0.4%2Fimage%2F2.zarr&"
                "cell_identities="
                "http%3A%2F%2Flocalhost%3A4080%2Fwebclient%2F"
                "annotation%2F1&"
                "cell_id_column=cell_id&"
                "cell_label_column=label&"
                "expression="
                "http%3A%2F%2Flocalhost%3A4080%2Fwebclient%2F"
                "annotation%2F4&"
                "embeddings="
                "http%3A%2F%2Flocalhost%3A4080%2Fwebclient%2F"
                "annotation%2F2&"
                "embedding_x=UMAP_1&"
                "embedding_y=UMAP_2&"
                "molecules="
                "http%3A%2F%2Flocalhost%3A4080%2Fwebclient%2F"
                "annotation%2F3&"
                "molecule_id=id&"
                "molecule_label=gene&"
                "molecule_x=x&"
                "molecule_y=y&"
                "histograms=on&"
                "heatmap=on&"
                "status=on&"
                "description=on")
        config_data.POST = QueryDict(text)
        vc_dict = utils.create_config(config_data.POST, "dataset", 1, conn)
        assert expected_json == vc_dict
