from django.shortcuts import render
from rest_framework.generics import CreateAPIView,DestroyAPIView,RetrieveUpdateAPIView,ListCreateAPIView
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Tag, Videos
from .serializers import TagSerializer, VideosSerializer
# Create your views here.
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('-created_on')
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

# Videos Api
class CreateVideoView(ListCreateAPIView):
    queryset = Videos.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = VideosSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {"message": f"{instance.title} has been created successfully"},
            status=status.HTTP_201_CREATED
        )