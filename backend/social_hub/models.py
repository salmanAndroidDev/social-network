from django.db import models
from core.models import BaseModelMixin
from django.conf import settings

PUBLIC = 'public'
PRIVATE = 'private'


class PublicPostManager(models.Manager):
    """
        Manager to return public posts
    """

    def get_queryset(self):
        return super().get_queryset().filter(policy=PUBLIC)


class Post(BaseModelMixin):
    """
        Post model to save information related to each post
    """

    POLICY_CHOICE = (
        (PUBLIC, 'public'),
        (PRIVATE, 'only me')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='images/%Y/%m/%d/',
                             blank=True)
    body = models.TextField()
    policy = models.CharField(choices=POLICY_CHOICE,
                              max_length=10,
                              default=PRIVATE)

    objects = models.Manager()
    public = PublicPostManager()  # customize manager for public posts

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
