from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import User, WhiteListedEmails
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class WhiteListedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteListedEmails
        fields = ['email']
    def validate_email(self, value):
        return value.lower().strip()
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class UpdateRetrieveSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "image_url",
            "role",
            "password",
            "password2",   # ✅ comma here
            "created_at",
        ]
        read_only_fields = ["id", "email", "role", "created_at"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        # Only validate if password is being updated
        if password or password2:
            if password != password2:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match"}
                )

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = "email_or_username"  
    email_or_username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_username = attrs.get("email_or_username")
        password = attrs.get("password")

        user = authenticate(username=email_or_username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        # Generate token
        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["full_name"] = user.full_name
        token["email"] = user.email
        token["role"] = user.role
        return token

    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password', 'password2']

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password" : "Password did not match"})
        return super().validate(attrs)
    def validate_email(self, value):
        value = value.lower().strip()

        if not WhiteListedEmails.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is not authorized for registration."
            )

        return value
    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email= validated_data['email'],
            full_name = validated_data['full_name'],
            password= validated_data['password'],
        )
        return user
    
class SuperAdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password": "Password did not match"})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password2', None)
        # Force role to superadmin
        user = User.objects.create_superuser(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
        )
        return user