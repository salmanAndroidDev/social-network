from django.db import models
from core.models import BaseModelMixin
from django.conf import settings


class Post(BaseModelMixin):
    """
        Post model to save information related to each post
    """
    PUBLIC = 'public'
    PRIVATE = 'private'

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

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
