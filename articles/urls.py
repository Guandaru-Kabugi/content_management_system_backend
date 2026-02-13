from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.CreateArticleView.as_view(), name="Create_Article"),
    path("article/<int:pk>/", views.UpdateGetDeleteAnArticle.as_view(), name="article-detail")
]