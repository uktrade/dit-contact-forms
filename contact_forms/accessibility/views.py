from django.views.generic import TemplateView


class AccessibilityView(TemplateView):
    """
    Generic class based template view for privacy nad conditions page

    """

    template_name = "accessibility/accessibility.html"
