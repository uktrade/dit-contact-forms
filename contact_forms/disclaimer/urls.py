from django.urls import re_path

from contact_forms.disclaimer import views

app_name = "disclaimer"

urlpatterns = [re_path("", views.DisclaimerView.as_view(), name="disclaimer")]
