from django.urls import re_path

from privacy_terms_and_conditions import views

app_name = "privacy_terms_and_conditions"

urlpatterns = [

    re_path(
        "",
        views.PrivacyTermsAndConditionsView.as_view(),
        name="terms_and_conditions",
    ),
]