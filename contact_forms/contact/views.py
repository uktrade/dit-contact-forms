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
        return False

    location = step_one_cleaned_data.get("location")

    return location == LocationChoices.EXPORTING_FROM_THE_UK


class ContactFormWizardView(SessionWizardView):
    condition_dict = {"step_two": display_step_two}
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        context = self.process_form_data(form_list)

        if context["type"] == "Zendesk":
            resp = ContactFormWizardView.send_to_zendesk(context)
        else:
            resp = ContactFormWizardView.send_mail(context)

        logger.info("FORM Submittion response: {} ".format(resp))
        logger.info("FORM Submittion response json: {} ".format(resp.json()))

        data = [form.cleaned_data for form in form_list]

        logger.info("FORM Data: ", data)

        return render(self.request, "contact/done.html", {"form_data": data})

    def render_next_step(self, form, **kwargs):
        """
        override next steps for step five if enquiry_topic is
        Commodity codes, tariffs and measures, import procedures
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

    @staticmethod
    def process_form_data(form_list):  # noqa: C901
        form_data = [form.cleaned_data for form in form_list]

        context = {
            "subject": "New CHEG Enquiry",
            "subdomain": settings.ZENDESK_SUBDOMAIN,
            "IEE_GA_GTM": settings.IEE_GA_GTM,
        }

        enquiry_topic = None
        for form in form_data:
            """
            check and store first question response in context
            """
            if "location" in form.keys():
                context["location"] = form["location"].label
            """
            check and store the second question response in context
            """
            if "enquiry_topic" in form.keys():
                context["topic"] = form["enquiry_topic"].label
                enquiry_topic = form["enquiry_topic"]
            """
            check and store the sender name, email and message in context
            """
            if "email_address" in form.keys():
                context["email_address"] = form["email_address"]
            if "name" in form.keys():
                context["name"] = form["name"]
            if "message" in form.keys():
                context["message"] = form["message"]

        if enquiry_topic == TopicChoices.EXPORTING_EXPLICIT:
            context["type"] = "email"
            context["recipient_email"] = settings.EU_EXIT_DIT_EMAIL
            context["recipient_fullname"] = settings.EU_EXIT_DIT_FULLNAME
            context["service_name"] = settings.ZENDESK_EU_EXIT_SERVICE_NAME
        elif enquiry_topic == TopicChoices.EXPORTING_GENERAL:
            context["type"] = "Zendesk"
            context["recipient_email"] = settings.EU_EXIT_EMAIL
            context["recipient_fullname"] = settings.EU_EXIT_FULLNAME
            context["service_name"] = settings.ZENDESK_EU_EXIT_SERVICE_NAME
        else:
            context["type"] = "Zendesk"
            context["recipient_email"] = settings.FEEDBACK_EMAIL
            context["recipient_fullname"] = settings.FEEDBACK_FULLNAME
            context["service_name"] = settings.ZENDESK_CHEG_SERVICE_NAME

        template = get_template("contact/contact_message_tmpl.txt")
        context["content"] = template.render(context)

        context["spam_control"] = helpers.SpamControl(contents=context["content"])

        context["sender"] = helpers.Sender(
            country_code="", email_address=[context["email_address"]]
        )

        context[
            "form_url"
        ] = "http://contact.check-duties-customs-exporting-goods.service.gov.uk/"

        return context

    @staticmethod
    def send_mail(context):
        email_form = ZendeskEmailForm(data={"message": context["content"]})
        assert email_form.is_valid()
        resp = email_form.save(
            recipients=[context["recipient_email"]],
            subject=context["subject"],
            reply_to=[context["email_address"]],
            form_url=context["form_url"],
        )
        return resp

    @staticmethod
    def send_to_zendesk(context):
        zendesk_form = ZendeskForm(
            data={
                "message": context["content"],
                "email_address": context["email_address"],
                "name": context["name"],
            }
        )
        assert zendesk_form.is_valid()
        resp = zendesk_form.save(
            email_address=context["email_address"],
            full_name=context["name"],
            form_url=context["form_url"],
            service_name=context["service_name"],
            spam_control=context["spam_control"],
            sender=context["sender"],
            subject=context["subject"],
            subdomain=context["subdomain"],
        )
        return resp
