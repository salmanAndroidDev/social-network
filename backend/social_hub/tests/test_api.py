from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Post


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PrivateUserAPITest(TestCase):
    """Test API request for authenticated user"""

    def setUp(self):
        self.user = create_user(
            email='Salman@gmail.com',
            password='test1234',
            name='Salman Barani'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        """Test that user can create post"""

        payload = {'title': 'title1',
                   'body': 'some body here',
                   'policy': 'public'}
        url = reverse('create_post')
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        for key in payload.keys():
            self.assertEqual(response.data[key], payload[key])


