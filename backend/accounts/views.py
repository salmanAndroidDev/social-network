from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import Contact

from .serializers import UserSerializer, AuthTokenSerializer, \
    ChangeStatusSerializer
from core.views import AuthenticationMixin


class RegisterUserView(generics.CreateAPIView):
    """
        Create a new user in the platform
    """
    serializer_class = UserSerializer


class AuthTokenView(ObtainAuthToken):
    """
        Create a new auth token for user
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ChangeStatusView(AuthenticationMixin, APIView):
    """
        API endpoint to change user status
    """
    serializer_class = ChangeStatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user,
                                           data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveUserListView(generics.ListAPIView):
    """
        API endpoint to get list of active users
    """
    queryset = get_user_model().objects.filter(status='active')
    serializer_class = UserSerializer


class FollowAPIView(AuthenticationMixin, APIView):
    """
        API endpoint to follow active users
    """

    def get(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(get_user_model(),
                                           email=kwargs.get('email'),
                                           status='active')
        Contact.objects.create(follow_from=request.user,
                               follow_to=user_to_follow)
        return Response({'message': 'success'}, status=status.HTTP_201_CREATED)


class UnFollowAPIView(AuthenticationMixin, APIView):
    """
        API endpoint to unfollow
    """

    def get(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(get_user_model(),
                                             email=kwargs.get('email'))
        Contact.objects.filter(follow_from=request.user,
                               follow_to=user_to_unfollow).delete()

        return Response({'message': 'success'},
                        status=status.HTTP_204_NO_CONTENT)


class FollowingListAPIView(AuthenticationMixin, generics.ListAPIView):
    """
        API endpoint to retrieve list of following users
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.following.all()
