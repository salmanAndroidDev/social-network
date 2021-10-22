from django.urls import path
from . import views

urlpatterns = [
    path('post/',
         views.CreatePostView.as_view(),
         name='create_post')
]
