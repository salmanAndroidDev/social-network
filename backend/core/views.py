from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class AuthenticationMixin:
    """
        Mixin for all Views that require authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
