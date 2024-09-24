"""Integration tests for all pages."""

from omeroweb.testlib import IWebTest, get
from django.urls import reverse


class TestLoadPage(IWebTest):
    """Tests loading the index page."""
    USER_NAME = "test_user"
    USER_GROUP = "TestGroup"
    USER_PWD = "password"

    def test_load_index(self):
        """Test loading the app home page."""
        django_client = self.new_django_client(TestLoadPage.USER_NAME,
                                               TestLoadPage.USER_PWD)
        index_url = reverse("vitessce_tab")
        # asserts we get a 200 response code etc
        rsp = get(django_client, index_url)
        html_str = rsp.content.decode()
        assert "React App" in html_str

    def test_load_openwith(self):
        """Test the openwith page."""
        django_client = self.new_django_client(TestLoadPage.USER_NAME,
                                               TestLoadPage.USER_PWD)
        openwith_url = "http://localhost:4080/omero_vitessce/open/?image=1"
        # asserts we get a 200 response code etc
        rsp = get(django_client, openwith_url)
        html_str = rsp.content.decode()
        assert "There are no config files attached!" in html_str
