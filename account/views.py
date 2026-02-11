from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView,DestroyAPIView,RetrieveUpdateAPIView,ListCreateAPIView
from .serializers import WhiteListedEmailSerializer,MyTokenObtainPairSerializer, RegisterSerializer,SuperAdminRegisterSerializer, UpdateRetrieveSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User,WhiteListedEmails
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsSuperAdmin

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CreateWhiteListedEmails(ListCreateAPIView):
    queryset = WhiteListedEmails.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = WhiteListedEmailSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {"message": f"{instance.email} has been whitelisted successfully"},
            status=status.HTTP_201_CREATED
        )


class RegisterView(CreateAPIView):
    queryset = User.objects.all() 
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": f"User with the email {user.email} has been created"},
            status=status.HTTP_201_CREATED
        )

class SuperAdminRegisterView(CreateAPIView):
    serializer_class = SuperAdminRegisterSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": f"Superadmin '{user.username}' created successfully"},
            status=201
        )


class WhiteListedEmailDelete(DestroyAPIView):
    queryset = WhiteListedEmails.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        email = instance.email

        # Remove from whitelist
        self.perform_destroy(instance)

        # Deactivate any users with that email
        updated_count = User.objects.filter(
            email__iexact=email
        ).update(is_active=False)

        return Response(
            {
                "message": f"{email} removed from whitelist",
                "users_deactivated": updated_count
            },
            status=status.HTTP_200_OK
        )


    
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        current_user = request.user

        # Prevent self-deletion
        if user_to_delete.id == current_user.id:
            return Response(
                {"detail": "You cannot delete yourself."},
                status=status.HTTP_403_FORBIDDEN
            )

        user_email = user_to_delete.email

        # Delete user
        self.perform_destroy(user_to_delete)

        # Delete whitelist entry if it exists
        WhiteListedEmails.objects.filter(
            email__iexact=user_email
        ).delete()

        return Response(
            {"message": f"User {user_email} deleted successfully"},
            status=status.HTTP_200_OK
        )
    
class UpdateGetUserView(RetrieveUpdateAPIView):
    serializer_class = UpdateRetrieveSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user
