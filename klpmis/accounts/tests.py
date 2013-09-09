from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class TestViewsBasic(TestCase):
    def setUp(self):
        test_group_1 = Group(name='test_group_1')
        test_group_1.save()
        test_group_2 = Group(name='test_group_2')
        test_group_2.save()
        test_group_3 = Group(name='test_group_3')
        test_group_3.save()

        self.user = \
            User.objects.create_superuser(username="foo",
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

    def test_user_auth(self):
        response = self.client.get(reverse("user_auth"))
        self.assertEqual("False", response.content)
        self.client.login(username="foo", password="bar")
        response = self.client.get(reverse("user_auth"))
        self.assertEqual("True", response.content)

    def test_add_user_without_login(self):
        form_data = {'username': 'test1',
                     'password1': 'test1',
                     'password2': 'test1',
                     'groups': [1, 2, 3]}
        response = self.client.post(reverse('accounts_add_user'),
                                    form_data)
        self.assertEqual(302, response.status_code)

    def test_add_user_with_login(self):
        form_data = {'username': 'test1',
                     'password1': 'test1',
                     'password2': 'test1',
                     'groups': [1, 2, 3]}
        self.client.login(username="foo", password="bar")
        response = self.client.post(reverse('accounts_add_user'),
                                    form_data)
        self.assertEqual(302, response.status_code)
