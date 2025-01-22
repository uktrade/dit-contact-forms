from django import forms
from django.db import models

from directory_forms_api_client.forms import ZendeskAPIForm, EmailAPIForm


class EnquiryTypeChoices(models.IntegerChoices):
    EXPORTING_HELP = 1, "Exporting from the UK"
    TECHNICAL_HELP = 2, "Technical help with using the service"


class TopicChoices(models.IntegerChoices):
    CUSTOMS_DECLARATIONS_AND_PROCEDURES = (
        1,
        "Customs declarations and procedures, duties and tariff rates",
    )
    COMMODITY_CODES = 2, "Commodity codes"
    EXPORTING_SPECIFIC = (
        3,
        "Exporting animals, plants or food, environmental regulations, sanitary & phytosanitary regulations",
    )
    EXPORTING_GENERAL = 4, "Exporting any other goods"


class BaseStepForm(forms.Form):
    def get_context(self):
        if not self.cleaned_data:
            raise Exception("Must be cleaned.")

        ctx = {}
        for field in self.ContextMeta.fields:
            value = self.cleaned_data[field]
            if isinstance(value, models.IntegerChoices):
                value = value.label
            ctx[field] = value

        return ctx


class ContactFormStepOne(BaseStepForm):
    class ContextMeta:
        fields = ["enquiry_type"]

    enquiry_type = forms.TypedChoiceField(
        choices=EnquiryTypeChoices.choices,
        coerce=lambda x: EnquiryTypeChoices(int(x)),
        label="What would you like to ask us about or give feedback on?",
        required=True,
        widget=forms.RadioSelect,
    )


class ContactFormStepTwo(BaseStepForm):
    class ContextMeta:
        fields = ["enquiry_topic"]

    enquiry_topic = forms.TypedChoiceField(
        choices=TopicChoices.choices,
        coerce=lambda x: TopicChoices(int(x)),
        label="What would you like to ask us about or give feedback on?",
        required=True,
        widget=forms.RadioSelect,
    )


class ContactFormStepThree(BaseStepForm):
    class ContextMeta:
        fields = ["name", "email_address", "message"]

    name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(
        help_text="Do not include personal or financial information, like your National Insurance number or credit card details.",  # noqa: E501
        label="Tell us how we can help",
        widget=forms.Textarea,
        required=True,
    )
    terms_and_conditions = forms.BooleanField(required=True)


class ZendeskForm(ZendeskAPIForm):

    # need a test commit needs more words
    # another line here

    # note that the base form provides `requester_email` email field
    name = forms.CharField()
    email_address = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class ZendeskEmailForm(EmailAPIForm):
    message = forms.CharField()

    @property
    def text_body(self):
        """Override text_body to text templte of email body."""

        text = str(self.cleaned_data["message"])
        return text

    @property
    def html_body(self):
        """Override html_body to return html template of email body."""
        cleaned = str(self.cleaned_data["message"]).replace("\n", "<br />")
        cleaned_html = "<p>" + cleaned + "</p>"
        return cleaned_html
