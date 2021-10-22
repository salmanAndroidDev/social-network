from django.urls import path
from . import views

urlpatterns = [
    path('register/',
         views.RegisterUserView.as_view(),
         name='register'),

    path('token/',
         views.AuthTokenView.as_view(),
         name='token'),

    path('change-status/',
         views.ChangeStatusView.as_view(),
         name='change_status'),

    path('active-users/',
         views.ActiveUserListView.as_view(),
         name='active_users'),

    path('follow/<email>/',
         views.FollowAPIView.as_view(),
         name='follow'),

    path('unfollow/<email>/',
         views.UnFollowAPIView.as_view(),
         name='unfollow'),

    path('following/',
         views.FollowingListAPIView.as_view(),
         name='following'),

]
