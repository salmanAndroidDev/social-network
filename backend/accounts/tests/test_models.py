from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Contact


def sample_user(email='test@gmail.com', password='test1234'):
    """Create sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class TestModel(TestCase):
    def setUp(self):
        self.user1 = sample_user(email='user1@gmail.com')
        self.user2 = sample_user(email='user2@gmail.com')
        self.user3 = sample_user(email='user3@gmail.com')

    def test_create_user_with_email_successfully(self):
        """Test create user with only email and password"""
        email = 'salman@gmail.com'
        password = 'something1234'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password, )
        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_make_new_user_email_normalized(self):
        """Test make new user email normalized"""
        email = "salman@GMAIL.COME"
        user = get_user_model().objects.create_user(email=email,
                                                    password="test1234")

        self.assertEqual(user.email, email.lower())

    def test_make_user_invalid_email(self):
        """Test raise error if email is not valid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None,
                                                 password="test1234")

    def test_create_super_user(self):
        "Test creating a new super user"
        user = get_user_model().objects.create_superuser(
            email="jamshid@gmail.com",
            password="test1234")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_can_follow(self):
        """Test that users can follow each other"""
        user1, user2, user3 = self.user1, self.user2, self.user3
        Contact.objects.create(follow_from=user1, follow_to=user2)
        Contact.objects.create(follow_from=user1, follow_to=user3)
        user1.refresh_from_db()
        self.assertIn(user2, user1.following.all())
        self.assertIn(user3, user1.following.all())

    def test_error_for_same_follower_and_following(self):
        """Throw a value error when following and follower are same"""
        with self.assertRaises(ValueError):
            Contact.objects.create(follow_to=self.user1,
                                   follow_from=self.user1)
