from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Create your tests here.

class RegisterTestCase(APITestCase):
    def test_register(self):
        data ={
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "Password@123",
            "password2" : "Password@123"
        }