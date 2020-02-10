from directory_forms_api_client.forms import ZendeskAPIForm, EmailAPIForm
from django import forms
from django.forms import fields

LOCATION_CHOICES = ((1, "Exporting from the UK"), (2, "Transition period enquiries"),
                    (3, "Technical help with using the service"))

TOPIC_CHOICES = (
    (
        1,
        "Customs declarations and procedures, commodity codes, duties and tariff rates",
    ),
    (
        2,
        "Exporting animals, plants or food, environmental regulations, sanitary & phytosanitary regulations",
    ),
    (3, "Exporting any other goods"),
)


class ContactFormStepOne(forms.Form):
    location = forms.ChoiceField(
        choices=LOCATION_CHOICES, widget=forms.RadioSelect, required=True
    )
    location.label = "What would you like to ask us about or give feedback on?"


class ContactFormStepTwo(forms.Form):
    enquiry_topic = forms.ChoiceField(
        choices=TOPIC_CHOICES, widget=forms.RadioSelect, required=True
    )
    enquiry_topic.label = "What would you like to ask us about or give feedback on?"


class ContactFormStepThree(forms.Form):
    name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    terms_and_conditions = forms.BooleanField(required=True)

    message.label = "Tell us how we can help"
    message.help_text = "Do not include personal or financial information, like your National Insurance number or credit card details."

    class Meta:
        fields = ["message", "name", "email_address", "terms_and_conditions"]
        error_messages = {
            "message": {
                "required": "Enter a message",
                "max_length": "Message needs to be less than 1,000 characters",
            },
            "name": {
                "required": "Enter your fullname",
                "max_length": "Name entered needs to be less than 255 characters",
            },
            "email_address": {
                "required": "Enter your email address",
                "invalid": "Enter an email address in the correct format, like name@example.com",
            },
            "terms_and_conditions": {
                "required": "Enter your email address",
                "invalid": "Enter an email address in the correct format, like name@example.com",
            },
        }


class ZendeskForm(ZendeskAPIForm):
    # note that the base form provides `requester_email` email field
    name = forms.CharField()
    email_address = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class ZendeskEmailForm(EmailAPIForm):
    message = fields.CharField()

    @property
    def text_body(self):
        ''' Override text_body to text templte of email body.'''

        text = str(self.cleaned_data['message'])
        return text

    @property
    def html_body(self):
        ''' Override html_body to return html template of email body.'''
        cleaned = str(self.cleaned_data['message']).replace("\n", "<br />")
        cleaned_html = '<p>' + cleaned + '</p>'
        return cleaned_html
