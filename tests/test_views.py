import logging

from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, Client

from contact_forms.contact.forms import (
    ContactFormStepOne,
    ContactFormStepThree,
    ContactFormStepTwo,
    EnquiryTypeChoices,
    TopicChoices,
)
from contact_forms.contact.views import CheckHowToExportGoodsContactView

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.INFO)


class ContactFormViewTestCase(SimpleTestCase):
    """
    Test Feedback View
    """

    def setUp(self):
        self.client = Client()
        self.wizard_url = "/enquiry/step_one"
        self.wizard_step_two_url = "/enquiry/step_two"
        self.wizard_step_three_url = "/enquiry/step_three"
        self.wizard_step_done_url = "/enquiry/done"

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
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_two_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_two",
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
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_two_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_two",
                "step_two-enquiry_topic": 2,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            settings.HMRC_TARIFF_CLASSIFICATION_SERVICE_URL,
            fetch_redirect_response=False,
        )

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    def test_exporting_specific_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_two_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_two",
                "step_two-enquiry_topic": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_three_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_done_url)

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    def test_exporting_general_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_two_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_two",
                "step_two-enquiry_topic": 4,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_three_url)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_done_url)

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    def test_technical_help_wizard_steps_flow(
        self, EmailAPIForm_save, ZendeskAPIForm_save
    ):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            {
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": EnquiryTypeChoices.TECHNICAL_HELP,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_three_url)

        response = self.client.post(
            self.wizard_step_three_url,
            {
                "check_how_to_export_goods_contact_view-current_step": "step_three",
                "step_three-message": "Test message",
                "step_three-name": "Test name",
                "step_three-email_address": "test@example.com",
                "step_three-terms_and_conditions": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.wizard_step_done_url)

    def test_form_wizard_errors(self):
        response = self.client.get(self.wizard_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 23,
            },
        )
        self.assertContains(
            response,
            '<span id="enquiry_type-error" class="govuk-error-enquiry_type">enquiry_type</span>',
            status_code=200,
            html=True,
        )

        response = self.client.post(
            self.wizard_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_one",
                "step_one-enquiry_type": 1,
            },
        )
        response = self.client.post(
            self.wizard_step_two_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_two",
                "step_two-enquiry_topic": 17,
            },
        )
        self.assertContains(
            response,
            '<span id="enquiry_topic-error" class="govuk-error-enquiry_topic">enquiry_topic</span>',
            status_code=200,
            html=True,
        )

        response = self.client.post(
            self.wizard_step_three_url,
            data={
                "check_how_to_export_goods_contact_view-current_step": "step_three",
            },
        )
        self.assertContains(
            response,
            '<a href="#name"class="error">Enter your full name</a>',
            status_code=200,
            html=True,
        )
        self.assertContains(
            response,
            """<a href="#email_address"class="error">
                Enter an email address in the correct format, like name@example.com</a>""",
            status_code=200,
            html=True,
        )
        self.assertContains(
            response,
            '<a href="#message"class="error">Ask us a question or give us feedback</a>',
            status_code=200,
            html=True,
        )
        self.assertContains(
            response,
            '<a href="#terms_and_conditions"class="error">Tick the box to agree to the terms and conditions</a>',
            status_code=200,
            html=True,
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

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.ZendeskAPIForm.is_valid")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    @patch("formtools.wizard.views.NamedUrlSessionWizardView.get_cleaned_data_for_step")
    def test_done_submissions_tech_help(
        self, get_clean_data, EmailAPIForm_save, valid_form, ZendeskAPIForm_save
    ):

        view = CheckHowToExportGoodsContactView()
        view.request = "request_mock"

        get_clean_data.return_value = {
            "enquiry_type": EnquiryTypeChoices.TECHNICAL_HELP
        }

        form_one = ContactFormStepOne()
        form_one.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_one"],
            "enquiry_type": "2",
        }
        form_three = ContactFormStepThree()
        form_three.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_three"],
            "message": "Test Message",
            "name": "Test McTest",
            "email_address": "test@test.com",
            "terms_and_conditions": "on",
        }

        form_list = [form_one, form_three]
        valid_form.return_value = True

        view.done(form_list, {})

        EmailAPIForm_save.assert_not_called()
        ZendeskAPIForm_save.assert_called()
        call_list = ZendeskAPIForm_save.call_args

        expected_call_args = {
            "email_address": "test@test.com",
            "full_name": "Test McTest",
            "form_url": "http://contact.check-duties-customs-exporting-goods.service.gov.uk/",
            "service_name": "check_export_duties",
            "sender": {
                "email_address": ["test@test.com"],
                "country_code": "",
                "ip_address": None,
            },
            "subject": "New CHEG Enquiry",
            "subdomain": settings.ZENDESK_SUBDOMAIN,
        }

        for key, value in expected_call_args.items():
            assert (key, value) in call_list.kwargs.items()

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.ZendeskAPIForm.is_valid")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    @patch("formtools.wizard.views.NamedUrlSessionWizardView.get_cleaned_data_for_step")
    def test_done_submissions_export_specific(
        self, get_clean_data, EmailAPIForm_save, valid_form, ZendeskAPIForm_save
    ):

        view = CheckHowToExportGoodsContactView()
        view.request = "request_mock"

        def side_effect_choice(input):
            if input == "step_one":
                return {"enquiry_type": EnquiryTypeChoices.EXPORTING_HELP}
            else:
                return {"enquiry_topic": TopicChoices.EXPORTING_SPECIFIC}

        get_clean_data.side_effect = side_effect_choice

        form_one = ContactFormStepOne()
        form_one.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_one"],
            "enquiry_type": "2",
        }
        form_two = ContactFormStepTwo()
        form_two.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_two"],
            "enquiry_topic": "3",
        }
        form_three = ContactFormStepThree()
        form_three.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_three"],
            "message": "Test Message",
            "name": "Test McTest",
            "email_address": "test@test.com",
            "terms_and_conditions": "on",
        }

        form_list = [form_one, form_two, form_three]
        valid_form.return_value = True

        view.done(form_list, {})

        EmailAPIForm_save.assert_called()
        ZendeskAPIForm_save.assert_not_called()
        call_list = EmailAPIForm_save.call_args

        expected_call_args = {
            "recipients": [settings.EU_EXIT_DIT_EMAIL],
            "subject": "New CHEG Enquiry",
            "reply_to": ["test@test.com"],
            "form_url": settings.FORM_URL,
        }

        for key, value in expected_call_args.items():
            assert (key, value) in call_list.kwargs.items()

    @patch("contact_forms.contact.forms.ZendeskAPIForm.save")
    @patch("contact_forms.contact.forms.ZendeskAPIForm.is_valid")
    @patch("contact_forms.contact.forms.EmailAPIForm.save")
    @patch("formtools.wizard.views.NamedUrlSessionWizardView.get_cleaned_data_for_step")
    def test_done_submissions_export_general(
        self, get_clean_data, EmailAPIForm_save, valid_form, ZendeskAPIForm_save
    ):

        view = CheckHowToExportGoodsContactView()
        view.request = "request_mock"

        def side_effect_choice(input):
            if input == "step_one":
                return {"enquiry_type": EnquiryTypeChoices.EXPORTING_HELP}
            else:
                return {"enquiry_topic": TopicChoices.EXPORTING_GENERAL}

        get_clean_data.side_effect = side_effect_choice

        form_one = ContactFormStepOne()
        form_one.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_one"],
            "enquiry_type": "2",
        }
        form_two = ContactFormStepTwo()
        form_two.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_two"],
            "enquiry_topic": "3",
        }
        form_three = ContactFormStepThree()
        form_three.cleaned_data = {
            "check_how_to_export_goods_contact_view-current_step": ["step_three"],
            "message": "Test Message",
            "name": "Test McTest",
            "email_address": "test@test.com",
            "terms_and_conditions": "on",
        }

        form_list = [form_one, form_two, form_three]
        valid_form.return_value = True

        view.done(form_list, {})

        EmailAPIForm_save.assert_not_called()
        ZendeskAPIForm_save.assert_called()
        call_list = ZendeskAPIForm_save.call_args

        expected_call_args = {
            "email_address": "test@test.com",
            "full_name": "Test McTest",
            "form_url": "http://contact.check-duties-customs-exporting-goods.service.gov.uk/",
            "service_name": "eu_exit",
            "sender": {
                "email_address": ["test@test.com"],
                "country_code": "",
                "ip_address": None,
            },
            "subject": "New CHEG Enquiry",
            "subdomain": settings.ZENDESK_SUBDOMAIN,
        }

        for key, value in expected_call_args.items():
            assert (key, value) in call_list.kwargs.items()
