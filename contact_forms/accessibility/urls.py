from django.urls import re_path

from contact_forms.accessibility import views

app_name = "accessibility"

urlpatterns = [re_path("", views.AccessibilityView.as_view(), name="accessibility")]
