from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TestViewsBasic(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="foo",
                                             email="foo@example.com",
                                             password="bar")
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(302, response.status_code)
        self.client.login(username="foo", password="bar")
        response = self.client.get(reverse("index"))
        self.assertEqual(302, response.status_code)

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(200, response.status_code)
        post_data = {'username': 'foo', 'password': 'bar'}
        response = self.client.post(reverse("login"), post_data)
        self.assertEqual(302, response.status_code)

    def test_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(302, response.status_code)
        self.client.login(username="foo", password="bar")
        response = self.client.get(reverse("logout"))
        self.assertEqual(302, response.status_code)

    def test_klp_user_auth(self):
        response = self.client.get(reverse("klp_user_auth"))
        self.assertEqual("False", response.content)
        self.client.login(username="foo", password="bar")
        response = self.client.get(reverse("klp_user_auth"))
        self.assertEqual("True", response.content)
