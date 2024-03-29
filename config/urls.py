from django.conf import settings
from django.urls import path, re_path, include

from cookies import views as cookie_views
from healthcheck.views import HealthCheckView

handler404 = "core.views.error404handler"
handler500 = "core.views.error500handler"

urlpatterns = [
    # redirects to start page
    path("cookies/", cookie_views.CookiesView.as_view(), name="cookies"),
    path(
        "help/cookies/", cookie_views.CookieDetailsView.as_view(), name="cookie-details"
    ),
    path(
        "privacy-terms-and-conditions/",
        include("privacy_terms_and_conditions.urls", namespace="privacy"),
    ),
    path("disclaimer/", include("disclaimer.urls", namespace="disclaimer")),
    path("accessibility/", include("accessibility.urls", namespace="accessibility")),
    re_path(r"^check/$", HealthCheckView.as_view(), name="healthcheck"),
    path("", include("contact.urls", namespace="contact")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("", include(debug_toolbar.urls))] + urlpatterns
