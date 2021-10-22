from rest_framework import generics
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


class PostListView(AuthenticationMixin, generics.ListAPIView):
    """
        API endpoint to retrieve list of posts
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class FollowingPostListView(AuthenticationMixin, generics.ListAPIView):
    """
        API endpoint to retrieve list of following users posts
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        users = list(self.request.user.following.values_list("id", flat=True))
        users.append(self.request.user.id)  # include current user posts
        return Post.public.filter(user__id__in=users)
