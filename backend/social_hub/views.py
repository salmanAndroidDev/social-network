from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.views import AuthenticationMixin
from .models import Post
from .serializers import PostSerializer


class CreatePostView(AuthenticationMixin, generics.CreateAPIView):
    """
        API endpoint to create post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
