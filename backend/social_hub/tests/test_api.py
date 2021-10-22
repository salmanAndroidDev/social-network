from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Post
from ..serializers import PostSerializer
from accounts.models import Contact


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_followers(user):
    """create dummy following users for given user"""
    user1 = create_user(email='user1', password='asdf!@#$')
    Contact.objects.create(follow_from=user, follow_to=user1)

    user2 = create_user(email='user2', password='asdf!@#$')
    Contact.objects.create(follow_from=user, follow_to=user2)

    user3 = create_user(email='user3', password='asdf!@#$')
    Contact.objects.create(follow_from=user, follow_to=user3)

    return user1, user2, user3


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

    def test_get_list_of_posts(self):
        """Test to get list of posts"""
        user2 = create_user(email='u2@gmail.com', password='asd!@#$')
        Post.objects.create(user=self.user, title='1', body='1b')
        Post.objects.create(user=user2, title='2', body='2b')
        Post.objects.create(user=self.user, title='3', body='3b')
        serializer = PostSerializer(self.user.post_set, many=True)

        url = reverse('my_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serializer.data)

    def test_get_posts_of_followings(self):
        """Test to get list of following users posts"""
        u1, u2, u3 = create_followers(self.user)
        user2 = create_user(email='u2@gmail.com', password='asd!@#$')
        Post.objects.create(user=self.user, title='2', body='1b',
                            policy='public')
        Post.objects.create(user=u1, title='1', body='1b', policy='public')
        Post.objects.create(user=user2, title='3', body='2b', policy='public')
        Post.objects.create(user=u2, title='4', body='3b', policy='public')
        Post.objects.create(user=u3, title='5', body='3b', policy='public')
        Post.objects.create(user=u3, title='6', body='3b', policy='public')
        Post.objects.create(user=u3, title='7', body='3b', policy='private')
        users = list(self.user.following.values_list("id", flat=True))
        users.append(self.user.id)  # include current user posts
        serializer = PostSerializer(Post.public.filter(user__id__in=users),
                                    many=True)

        url = reverse('posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data, serializer.data)
