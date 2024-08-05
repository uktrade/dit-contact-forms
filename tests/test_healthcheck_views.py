from django.test import SimpleTestCase, Client

import xml.etree.ElementTree as ET


class TestViews(SimpleTestCase):
    """
    Test Healthcheck views
    """

    def setUp(self):
        self.anonymous_client = Client()

    def test_check_view(self):
        response = self.anonymous_client.get("/check/")
        tree = ET.fromstring(response.content)
        pingdom_status = tree[0].text
        pingdom_response_time = float(tree[1].text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pingdom_status, "OK")
        self.assertGreater(pingdom_response_time, 0)
        self.assertLess(pingdom_response_time, 1)
