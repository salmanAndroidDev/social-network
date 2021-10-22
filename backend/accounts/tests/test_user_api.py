from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from ..models import Contact
from ..serializers import UserSerializer

CREATE_USER_URL = reverse('register')
TOKEN_URL = reverse('token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user(email='u1@gmail.com',
                                 password='asdf!@#$',
                                 status='inactive')
        self.user2 = create_user(email='u2@gmail.com',
                                 password='asdf!@#$',
                                 status='active')
        self.user3 = create_user(email='u3@gmail.com',
                                 password='asdf!@#$',
                                 status='inactive')
        self.user4 = create_user(email='u4@gmail.com',
                                 password='asdf!@#$',
                                 status='active')

    def test_valid_user_success(self):
        """Test that user validated and created successfully"""
        payload = {
            'email': "salman@gmail.com",
            'password': 'test1234',
            'name': "Salman Barani"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test that user already exists"""
        payload = {"email": "jasom@gmail.com", "password": "tests1234",
                   "name": "Jasom Barani"}

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        """Test for short passwords < 5 characters"""
        payload = {'email': "salman@gmail.com", "password": 'pw',
                   "name": "Salman Barani"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            **res.data
        ).exists()
        self.assertFalse(user_exist)

    def test_tokes_is_created(self):
        """Test that token is returned after logging in"""
        payload = {'email': "salman@gmail.com", 'password': 'test1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_invalid_credential(self):
        """Test the token is not created when credentials is invalid"""
        payload = {'email': "salman@gmail.com", 'password': 'test1234'}
        wrong_payload = {'email': "salman@gmail.com", 'password': 'wrong'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, wrong_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_without_user(self):
        """Test the token is not created when user is not created"""
        payload = {'email': "salman@gmail.com", 'password': 'test1234'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_missing_field(self):
        """Test the token is not created when a field is missing"""
        payload = {'email': "salman@gmail.com", 'password': 'test1234'}
        wrong_payload = {'email': "salman@gmail.com"}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, wrong_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_get_list_of_active_users(self):
        """Test getting list of active users"""
        url = reverse('active_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 users are active


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

    def test_change_status_works(self):
        """Test that change status works as expected"""
        payload = {'status': 'inactive'}
        url = reverse('change_status')
        response = self.client.post(url, payload, )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertEqual(getattr(self.user, 'status'), payload['status'])

    def test_change_status_bad_input(self):
        """
            Test that changing status only works with active and inactive
            payloads
        """
        payload = {'status': 'wrong_input'}
        url = reverse('change_status')
        response = self.client.post(url, payload, )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(getattr(self.user, 'status'), 'active')

    def test_follow_user(self):
        """Test that following works as expected"""
        user2 = create_user(email='u2@gmail.com', password='asdf!@#$')
        url = reverse('follow', kwargs={'email': user2.email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.refresh_from_db()
        self.assertIn(user2, self.user.following.all())
        self.assertEqual(self.user.following.count(), 1)

    def test_unfollow_user(self):
        """Test to unfollow users"""
        user2 = create_user(email='u2@gmail.com', password='asdf!@#$')
        user3 = create_user(email='u3@gmail.com', password='asdf!@#$')
        user4 = create_user(email='u4@gmail.com', password='asdf!@#$')

        Contact.objects.create(follow_from=self.user, follow_to=user2)
        Contact.objects.create(follow_from=self.user, follow_to=user3)
        Contact.objects.create(follow_from=self.user, follow_to=user4)

        url = reverse('unfollow', kwargs={'email': user3.email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertNotIn(user3, self.user.following.all())
        self.assertEqual(self.user.following.count(), 2)

    def test_list_of_following(self):
        user2 = create_user(email='u2@gmail.com', password='asdf!@#$')
        user3 = create_user(email='u3@gmail.com', password='asdf!@#$')
        user4 = create_user(email='u4@gmail.com', password='asdf!@#$')

        Contact.objects.create(follow_from=self.user, follow_to=user2)
        Contact.objects.create(follow_from=self.user, follow_to=user3)
        Contact.objects.create(follow_from=self.user, follow_to=user4)
        serializer = UserSerializer(self.user.following.all(),many=True)

        url = reverse('following')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)