from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post


def sample_user(email='test@gmail.com', password='test1234'):
    """Create sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class TestModel(TestCase):

    def test_create_post(self):
        """Test that post can be created successfully"""
        data = {'user': sample_user(),
                'title': 'title1',
                'body': 'some body here',
                'policy': 'public'}

        post = Post.objects.create(**data)
        for key in data.keys():
            self.assertEqual(getattr(post, key), data[key])
