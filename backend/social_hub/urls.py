from django.urls import path
from . import views

urlpatterns = [
    path('post/',
         views.CreatePostView.as_view(),
         name='create_post'),

    path('my-posts/',
         views.PostListView.as_view(),
         name='my_posts'),

    path('posts/',
         views.FollowingPostListView.as_view(),
         name='posts')

]
