"""helpdesk_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from admin.views import admin_login_view
from cookies import views as cookie_views
from countries import views as country_views
from iee_contact import views as iee_contact_views
from healthcheck.views import HealthCheckView
from index import views as index


handler404 = "core.views.error404handler"
handler500 = "core.views.error500handler"

urlpatterns = [
    # redirects to start page
    path("", index.IndexRedirect.as_view(), name="index"),
    path("auth/", include("authbroker_client.urls", namespace="authbroker")),
    path("cookies/", cookie_views.CookiesView.as_view(), name="cookies"),

    path(
        "iee_contact/",
        iee_contact_views.IEEContactFormWizardView.as_view(),
        name="iee-contact-view",
    ),
    re_path(r"^check/$", HealthCheckView.as_view(), name="healthcheck"),

]


if settings.ADMIN_ENABLED:
    urlpatterns += [
        path("admin/login/", admin_login_view),
        path("admin/", admin.site.urls),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("", include(debug_toolbar.urls))] + urlpatterns
