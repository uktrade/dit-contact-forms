from django.urls import path, re_path

from contact_forms.contact import views

app_name = "contact"

enquiry_wizard_view = views.CheckHowToExportGoodsContactView.as_view(
    url_name="contact:enquiry-wizard-step",
)

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    re_path(
        r"^enquiry/(?P<step>.+)$",
        enquiry_wizard_view,
        name="enquiry-wizard-step",
    ),
    path(
        "enquiry",
        enquiry_wizard_view,
        name="enquiry-wizard",
    ),
]
