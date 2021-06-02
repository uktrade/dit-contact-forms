import enum
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from directory_forms_api_client import helpers
from formtools.wizard.views import SessionWizardView

from .forms import (
    ContactFormStepOne,
    ContactFormStepTwo,
    ContactFormStepThree,
    LocationChoices,
    TopicChoices,
    ZendeskForm,
    ZendeskEmailForm,
)

logger = logging.getLogger(__name__)

FORMS = [
    ("step_one", ContactFormStepOne),
    ("step_two", ContactFormStepTwo),
    ("step_three", ContactFormStepThree),
]

TEMPLATES = {step_name: f"contact/{step_name}.html" for step_name, _ in FORMS}

TOPIC_REDIRECTS = {
    TopicChoices.CUSTOMS_DECLARATIONS_AND_PROCEDURES: settings.HMRC_TAX_FORM_URL,
    TopicChoices.COMMODITY_CODES: settings.HMRC_TARIFF_CLASSIFICATION_SERVICE_URL,
}


def display_step_two(wizard):
    step_one_cleaned_data = wizard.get_cleaned_data_for_step("step_one")
    if not step_one_cleaned_data:
        return True

    location = step_one_cleaned_data.get("location")

    return location == LocationChoices.EXPORTING_FROM_THE_UK


class SendType(enum.Enum):
    ZENDESK = enum.auto()
    EMAIL = enum.auto()


class ContactFormWizardView(SessionWizardView):
    condition_dict = {"step_two": display_step_two}
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        send_type, context = self.process_form_data(form_list)

        if send_type == SendType.ZENDESK:
            resp = self.send_to_zendesk(context)
        else:
            resp = self.send_mail(context)

        logger.info("FORM Submittion response: %s", resp)
        logger.info("FORM Submittion response json: %s", resp.json())

        data = [form.cleaned_data for form in form_list]

        logger.info("FORM Data: %s", data)

        return render(self.request, "contact/done.html", {"form_data": data})

    def render_next_step(self, form, **kwargs):
        """
        return early and redirect on certain steps
        :param form: submitted form
        :param kwargs: passed keyword arguments
        :return: render to response
        """
        if "enquiry_topic" in form.cleaned_data and self.steps.next == "step_three":
            enquiry_topic = form.cleaned_data["enquiry_topic"]
            redirect_url = TOPIC_REDIRECTS.get(enquiry_topic)
            if redirect_url:
                return HttpResponseRedirect(redirect_url)

        return super(ContactFormWizardView, self).render_next_step(form, **kwargs)

    def process_form_data(self, form_list):
        context = {
            "subject": "New CHEG Enquiry",
        }

        for form in form_list:
            context.update(form.get_context())

        enquiry_topic = None
        form_data = [form.cleaned_data for form in form_list]
        for form in form_data:
            if "enquiry_topic" in form.keys():
                enquiry_topic = form["enquiry_topic"]
                break

        send_type = SendType.ZENDESK
        if enquiry_topic == TopicChoices.EXPORTING_EXPLICIT:
            send_type = SendType.EMAIL
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

        return send_type, context

    def send_mail(self, context):
        email_form = ZendeskEmailForm(data={"message": context["content"]})
        assert email_form.is_valid()
        resp = email_form.save(
            recipients=[context["recipient_email"]],
            subject=context["subject"],
            reply_to=[context["email_address"]],
            form_url=settings.FORM_URL,
        )
        return resp

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
