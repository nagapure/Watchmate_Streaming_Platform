from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models
# Create your tests here.

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Password@123')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name = "Netflix", about = " #1 Streaming platform", website = "https://www.netflix.com")
        
        
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Test Platform Description",
            "website": "https://www.netflix.com",
        }
        response = self.client.post(reverse('streamplatform-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_streamplatform_individual(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
