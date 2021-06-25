import logging

from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, Client

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.INFO)


class ContactFormViewTestCase(SimpleTestCase):
    """
    Test Feedback View
    """

    def setUp(self):
        self.client = Client()
        self.wizard_url = "/contact/"

    def test_initial_form_call(self):
        response = self.client.get(self.wizard_url)
        wizard = response.context["wizard"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wizard["steps"].current, "step_one")
        self.assertEqual(wizard["steps"].step0, 0)
        self.assertEqual(wizard["steps"].step1, 1)
        self.assertEqual(wizard["steps"].last, "step_three")
        self.assertEqual(wizard["steps"].prev, None)
        self.assertEqual(wizard["steps"].next, "step_two")
        self.assertEqual(wizard["steps"].count, 3)

    def test_customs_declarations_wizard_steps_flow(self):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_one",
                "step_one-location": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_two",
                "step_two-enquiry_topic": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, settings.HMRC_TAX_FORM_URL, fetch_redirect_response=False
        )

    def test_commodity_codes_wizard_steps_flow(self):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_one",
                "step_one-location": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_two",
                "step_two-enquiry_topic": 2,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            settings.HMRC_TARIFF_CLASSIFICATION_SERVICE_URL,
            fetch_redirect_response=False,
        )

    @patch("contact.forms.ZendeskAPIForm.save")
    @patch("contact.forms.EmailAPIForm.save")
    def test_exporting_specific_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_one",
                "step_one-location": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_two",
                "step_two-enquiry_topic": 3,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        EmailAPIForm_save.assert_called_with(
            form_url="http://contact.check-duties-customs-exporting-goods.service.gov.uk/",
            recipients=["EUExitDIT@defra.gov.uk"],
            reply_to=["test@example.com"],
            subject="New CHEG Enquiry",
        )
        ZendeskAPIForm_save.assert_not_called()

    @patch("contact.forms.ZendeskAPIForm.save")
    @patch("contact.forms.EmailAPIForm.save")
    def test_exporting_general_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_one",
                "step_one-location": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_two",
                "step_two-enquiry_topic": 4,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        EmailAPIForm_save.assert_not_called()
        ZendeskAPIForm_save.assert_called_with(
            email_address="test@example.com",
            form_url="http://contact.check-duties-customs-exporting-goods.service.gov.uk/",
            full_name="Test name",
            sender={"email_address": ["test@example.com"], "country_code": ""},
            service_name="eu_exit",
            spam_control={
                "contents": "\nTo euexit\n\nI would like to know more about Exporting from the UK\n\n\nI would like to know more about Exporting any other goods\n\n\nTest message\n\nThank you\nTest name\ntest@example.com\n",  # noqa: E501
            },
            subdomain="dit",
            subject="New CHEG Enquiry",
        )

    @patch("contact.forms.ZendeskAPIForm.save")
    @patch("contact.forms.EmailAPIForm.save")
    def test_technical_help_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_one",
                "step_one-location": 2,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "contact_form_wizard_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        EmailAPIForm_save.assert_not_called()
        ZendeskAPIForm_save.assert_called_with(
            email_address="test@example.com",
            form_url="http://contact.check-duties-customs-exporting-goods.service.gov.uk/",
            full_name="Test name",
            sender={"email_address": ["test@example.com"], "country_code": ""},
            service_name="check_export_duties",
            spam_control={
                "contents": "\nTo Live Services\n\nI would like to know more about Technical help with using the service\n\n\n\nTest message\n\nThank you\nTest name\ntest@example.com\n"  # noqa: E501
            },
            subdomain="dit",
            subject="New CHEG Enquiry",
        )

    def test_static_pages(self):
        disclaimer_response = self.client.get("/disclaimer/")
        self.assertEqual(disclaimer_response.status_code, 200)
        self.assertEqual(
            disclaimer_response.templates[0].name, "disclaimer/disclaimer.html"
        )

        accessibility_response = self.client.get("/accessibility/")
        self.assertEqual(accessibility_response.status_code, 200)
        self.assertEqual(
            accessibility_response.templates[0].name, "accessibility/accessibility.html"
        )

        privacy_response = self.client.get("/privacy-terms-and-conditions/")
        self.assertEqual(privacy_response.status_code, 200)
        self.assertEqual(
            privacy_response.templates[0].name, "privacy_terms_and_conditions.html"
        )

        cookies_response = self.client.get("/cookies/")
        self.assertEqual(cookies_response.status_code, 200)
        self.assertEqual(cookies_response.templates[0].name, "preferences.html")
