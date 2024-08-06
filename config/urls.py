from django.conf import settings
from django.urls import path, re_path, include

from contact_forms.cookies import views as cookie_views
from contact_forms.healthcheck.views import HealthCheckView

handler404 = "contact_forms.core.views.error404handler"
handler500 = "contact_forms.core.views.error500handler"

urlpatterns = [
    # redirects to start page
    path("cookies/", cookie_views.CookiesView.as_view(), name="cookies"),
    path(
        "help/cookies/", cookie_views.CookieDetailsView.as_view(), name="cookie-details"
    ),
    path(
        "privacy-terms-and-conditions/",
        include("contact_forms.privacy_terms_and_conditions.urls", namespace="privacy"),
    ),
    path(
        "disclaimer/", include("contact_forms.disclaimer.urls", namespace="disclaimer")
    ),
    path(
        "accessibility/",
        include("contact_forms.accessibility.urls", namespace="accessibility"),
    ),
    re_path(r"^check/$", HealthCheckView.as_view(), name="healthcheck"),
    path("", include("contact_forms.contact.urls", namespace="contact")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("", include(debug_toolbar.urls))] + urlpatterns
