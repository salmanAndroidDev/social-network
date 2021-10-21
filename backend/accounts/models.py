from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from core.models import BaseModelMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create user by email and password"""
        if not email:
            raise ValueError('user must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, ):
        """Creating superuser by email and password"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        User model to save user by email instead of username
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS_CHOICE = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE)
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICE,
                              max_length=10,
                              default=ACTIVE)
    following = models.ManyToManyField('self',
                                       through='Contact',
                                       symmetrical=False,
                                       related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Contact(BaseModelMixin):
    """
        Contact is an intermediary model for ManyToMany relationship
    """
    follow_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='rel_from_set',
                                    on_delete=models.CASCADE)
    follow_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_to_set',
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)
        unique_together = ('follow_from', 'follow_to')

    def save(self, **kwargs):
        """save contact only if the following and follower aren't the same"""
        if self.follow_from == self.follow_to:
            raise ValueError("follower a following can't be the dame")
        return super().save(**kwargs)

    def __str__(self):
        return f'{self.follow_from} follows {self.follow_to}'
