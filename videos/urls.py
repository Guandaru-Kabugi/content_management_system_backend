from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet,CreateVideoView,RetrieveUpdateVideoView,DestroyVideoView

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('videos/', CreateVideoView.as_view(), name='Create-Video'),
    path('videos/<int:id>/delete/', DestroyVideoView.as_view(), name='Destroy-Video'),
    path('videos/<int:id>/update/', RetrieveUpdateVideoView.as_view(), name='Update-Video'),
]
