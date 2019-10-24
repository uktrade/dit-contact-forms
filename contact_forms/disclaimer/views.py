from django.views.generic import TemplateView


class DisclaimerView(TemplateView):
    """
    Generic class based template view for privacy nad conditions page

    """

    template_name = "disclaimer/disclaimer.html"
