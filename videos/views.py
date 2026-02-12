from django.shortcuts import render
from rest_framework.generics import CreateAPIView,DestroyAPIView,RetrieveUpdateAPIView,ListCreateAPIView
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Tag, Videos
from .serializers import TagSerializer, VideosSerializer,VideosUpdateSerializer
# Create your views here.
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('-created_on')
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

# Videos Api
class CreateVideoView(ListCreateAPIView):
    queryset = Videos.objects.all().order_by('-posted_on')
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response(
            {
                "message": f"{response.data.get('title')} has been created successfully",
                "data": response.data
            },
            status=status.HTTP_201_CREATED
        )
class RetrieveUpdateVideoView(RetrieveUpdateAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": f"{instance.title} has been updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
class DestroyVideoView(DestroyAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"

    transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)

        return Response(
            {
                "message": f"{title} has been deleted successfully"
            },
            status=status.HTTP_200_OK
        )