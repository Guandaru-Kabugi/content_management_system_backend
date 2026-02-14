from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.CreatePostView.as_view(), name='Create-Post'),
    path("post/<int:pk>/", views.UpdateGetDeleteAPost.as_view(), name='post-detail')
]