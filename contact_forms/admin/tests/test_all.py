from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import TestCase, Client, override_settings

from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from user.models import User


class AdminSSOLoginTestCase(TestCase):

    """
    Asmin SSO tests
    """

    def setUp(self):
        self.client = Client()
        self.user = mixer.blend(
            User, email="test@test.com", is_staff=False, is_superuser=False
        )

    def test_login_authenticated_but_not_staff_leads_to_403_when_admin_enabled(self):
        self.client.force_login(self.user)
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 403)

    def test_login_authenticated_without_next_url_redirects_to_admin_when_admin_enabled(
        self
    ):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/")

    def test_login_authenticated_redirects_to_next_url_when_admin_enabled(self):
        self.user.is_staff = True
        self.user.save()
        session = self.client.session
        session["admin_next_url"] = "/whatever/"
        session.save()
        self.client.force_login(self.user)

        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/whatever/")

    def test_login_redirects_to_sso_login_when_admin_enabled(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login/")

    def test_login_saves_next_query_string_in_session_when_admin_enabled(self):
        self.client.get("/admin/login/?next=/whatever/")

        self.assertEqual(self.client.session["admin_next_url"], "/whatever/")
