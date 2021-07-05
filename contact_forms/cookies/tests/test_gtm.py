from django.test import SimpleTestCase

from cookies.templatetags.gtm import google_tag_manager
from cookies.templatetags.gtm import google_tag_manager_noscript


class GoogleTagManagerTestCase(SimpleTestCase):

    """
    Test Google Tag Manager Template Tags
    """

    def test_missing_container_id(self):
        with self.settings(IEE_GA_GTM=""):
            result = google_tag_manager()
            self.assertEqual(result, "<!-- missing GTM container id -->")

    def test_missing_container_id_noscript(self):
        with self.settings(IEE_GA_GTM=""):
            result = google_tag_manager_noscript()
            self.assertEqual(result, "<!-- missing GTM container id -->")
