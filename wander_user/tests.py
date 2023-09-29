from datetime import datetime
from unittest import skip
from django.urls import reverse
from .models import User
from rest_framework.test import APITestCase


class CreateUserTest(APITestCase):
    def test_create_user(self):
        response = self.client.post('/api/users/', {
            "username": "abc",
            "email": "abc@django.com",
            "password": "admin@123"

        })

        self.assertEqual(response.data['username'], 'abc')

        user = User.objects.get(username='abc')
        self.assertEqual(user.username, 'abc')


class GetTokenTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username="lion", password="admin@123", email="lion@django.com")

    def test_user_login(self):
        response = self.client.post('/api/jwt/create/', {
            "username": "lion",
            "password": "admin@123"
        })

        self.assertIn('access', response.data)


class GetUserInfoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="lucy",
                                             password="admin@123",
                                             email="lucy@django.com")
        response = self.client.post('/api/jwt/create/', {
            "username": "lucy",
            "password": "admin@123"
        })

        self.token = response.data.get('access')

    def test_get_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        response = self.client.get('/api/users/me/')

        self.assertEqual(response.data['username'], 'lucy')
