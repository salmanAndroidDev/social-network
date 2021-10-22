from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
        Post serializer to use for post creation
    """

    class Meta:
        model = Post
        fields = ('user', 'title', 'body', 'policy',)
        read_only_fields = ('user',)
