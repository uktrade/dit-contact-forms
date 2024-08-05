from unittest import skip

from django.test import RequestFactory
from django.test import SimpleTestCase

from contact_forms.core.views import error500handler


class CoreViewsTestCase(SimpleTestCase):

    """
    Test Error pages
    """

    @skip("Unknown as to whether test is still valid")
    def test_404_error(self):
        resp = self.client.get("/non_existant_path/")
        self.assertEqual(resp.status_code, 404)

    def test_500_error(self):
        req = RequestFactory().get("/contact/")
        resp = error500handler(req)
        self.assertEqual(resp.status_code, 500)
