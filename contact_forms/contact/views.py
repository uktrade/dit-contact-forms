import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy

from directory_forms_api_client import helpers
from formtools.wizard.views import NamedUrlSessionWizardView

from .forms import (
    ContactFormStepOne,
    ContactFormStepTwo,
    ContactFormStepThree,
    EnquiryTypeChoices,
    TopicChoices,
    ZendeskForm,
    ZendeskEmailForm,
)

logger = logging.getLogger(__name__)

TOPIC_REDIRECTS = {
    TopicChoices.CUSTOMS_DECLARATIONS_AND_PROCEDURES: settings.HMRC_TAX_FORM_URL,
    TopicChoices.COMMODITY_CODES: settings.HMRC_TARIFF_CLASSIFICATION_SERVICE_URL,
}


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("contact:enquiry-wizard")


def is_export_enquiry_type(enquiry_type_choice, on_default_path=False):
    """Returns a function to assert whether the wizard step should be shown
    based on the enquiry type selected.

    The `on_default_path` allows the returned function to return a default
    value if the enquiry type hasn't been filled in yet. This is important
    when we want to show the correct number of steps in the form.
    """

    def _is_type(wizard):
        step_one_cleaned_data = wizard.get_cleaned_data_for_step("step_one")
        if not step_one_cleaned_data:
            return on_default_path
        enquiry_type = step_one_cleaned_data["enquiry_type"]
        return enquiry_type == enquiry_type_choice

    return _is_type


class CheckHowToExportGoodsContactView(NamedUrlSessionWizardView):
    form_list = [
        ("step_one", ContactFormStepOne),
        ("step_two", ContactFormStepTwo),
        ("step_three", ContactFormStepThree),
    ]
    """
    Django will only include a given form when the condition method
    in the condition dictionary returns true. In this case, we want to
    include step_two form when the user has entered option 1 (Exporting from the UK)
    as the enquiry type in step 1.
    """
    condition_dict = {
        "step_two": is_export_enquiry_type(
            EnquiryTypeChoices.EXPORTING_HELP, on_default_path=True
        ),
    }

    def get_template_names(self):
        templates = {
            form_name: f"contact/{form_name}.html" for form_name in self.form_list
        }

        return [templates[self.steps.current]]

    def render_next_step(self, form, **kwargs):
        """
        Intercept rendering of next step and perform redirect if
        topic entered is a question for HMRC
        """
        if "enquiry_topic" in form.cleaned_data and self.steps.next == "step_three":
            enquiry_topic = form.cleaned_data["enquiry_topic"]
            redirect_url = TOPIC_REDIRECTS.get(enquiry_topic)
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
        return super(CheckHowToExportGoodsContactView, self).render_next_step(
            form, **kwargs
        )

    def send_to_zendesk(self, context):
        zendesk_form = ZendeskForm(
            data={
                "message": context["content"],
                "email_address": context["email_address"],
                "name": context["name"],
            }
        )
        assert zendesk_form.is_valid()
        spam_control = helpers.SpamControl(contents=context["content"])
        sender = helpers.Sender(
            country_code="", email_address=[context["email_address"]]
        )

        resp = zendesk_form.save(
            email_address=context["email_address"],
            full_name=context["name"],
            form_url=settings.FORM_URL,
            service_name=context["service_name"],
            spam_control=spam_control,
            sender=sender,
            subject=context["subject"],
            subdomain=settings.ZENDESK_SUBDOMAIN,
        )
        return resp

    def send_to_email(self, context):

        email_form = ZendeskEmailForm(data={"message": context["content"]})
        assert email_form.is_valid()
        resp = email_form.save(
            recipients=[context["recipient_email"]],
            subject=context["subject"],
            reply_to=[context["email_address"]],
            form_url=settings.FORM_URL,
        )
        return resp

    def process_form_data(self, form_list, enquiry_topic):
        context = {
            "subject": "New CHEG Enquiry",
        }

        for form in form_list:
            context.update(form.get_context())

        if enquiry_topic == TopicChoices.EXPORTING_SPECIFIC:
            context["recipient_email"] = settings.EU_EXIT_DIT_EMAIL
            context["recipient_fullname"] = settings.EU_EXIT_DIT_FULLNAME
            context["service_name"] = settings.ZENDESK_EU_EXIT_SERVICE_NAME
        elif enquiry_topic == TopicChoices.EXPORTING_GENERAL:
            context["recipient_email"] = settings.EU_EXIT_EMAIL
            context["recipient_fullname"] = settings.EU_EXIT_FULLNAME
            context["service_name"] = settings.ZENDESK_EU_EXIT_SERVICE_NAME
        else:
            context["recipient_email"] = settings.FEEDBACK_EMAIL
            context["recipient_fullname"] = settings.FEEDBACK_FULLNAME
            context["service_name"] = settings.ZENDESK_CHEG_SERVICE_NAME

        template = get_template("contact/contact_message_tmpl.txt")
        context["content"] = template.render(context)

        return context

    def done(self, form_list, form_dict, **kwargs):
        enquiry_topic = (
            self.get_cleaned_data_for_step("step_two")["enquiry_topic"]
            if self.get_cleaned_data_for_step("step_one")["enquiry_type"]
            == EnquiryTypeChoices.EXPORTING_HELP
            else ""
        )

        # Put form data into a context which can be more easily referred to
        # later in the done process
        context = self.process_form_data(form_list, enquiry_topic)

        if enquiry_topic == TopicChoices.EXPORTING_SPECIFIC:
            # Enquiry is intended for DEFRA regarding specific environmental related exports
            self.send_to_email(context)
        else:
            # Enquiry is intended for DBT regarding generic exporting
            self.send_to_zendesk(context)

        return render(self.request, "contact/done.html")
