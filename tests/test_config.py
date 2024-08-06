from django.test import SimpleTestCase
from django.apps import apps

from contact_forms.contact.apps import ContactConfig


class ContactConfigTestCase(SimpleTestCase):

    """
    Test app config
    """

    def test_apps(self):
        self.assertEqual(ContactConfig.name, "contact_forms.contact")
        self.assertEqual(apps.get_app_config("contact").name, "contact_forms.contact")
