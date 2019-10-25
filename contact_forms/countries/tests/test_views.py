import logging

from django.test import TestCase
from django.urls import reverse
from django.utils.functional import SimpleLazyObject

from countries.models import Country

logger = logging.getLogger(__name__)
# logging.disable(logging.NOTSET)
logger.setLevel(logging.INFO)


class CountriesViewsTestCase(TestCase):

    """
    Views tests
    """

    def test_session_has_no_origin_country_attribute(self):
        session = self.client.session
        self.assertRaises(KeyError, lambda: session["origin_country"])

    def test_request_has_origin_country_attribute(self):
        session = self.client.session
        session["origin_country"] = "AU"
        session.save()
        self.assertEqual(session["origin_country"], "AU")
