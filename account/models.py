from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        full_name=None,
        username=None,
        password=None,
        image_url=None,
        **extra_fields,
    ):
        if not email:
            raise ValidationError("An email address is required")
        if not username:
            raise ValidationError("A username is required")
        if not full_name:
            raise ValidationError("Full name is required")
        if not password:
            raise ValidationError("A password is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            role='admin',
            image_url=image_url,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password,
        full_name=None,
        username=None,
        image_url=None,
        **extra_fields,
    ):
        if not password:
            raise ValidationError("Superuser must have a password")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            role="superadmin",  # 👑 forced internally
            image_url=image_url,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("superadmin", "SuperAdmin"),
    )

    # Override username behavior (email-based login)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=300, unique=True)

    full_name = models.CharField(max_length=200)
    image_url = models.URLField(blank=True, null=True, max_length=1000)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="admin",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Sensible defaults
        if not self.username:
            self.username = self.email.split("@")[0]

        if not self.full_name:
            self.full_name = self.username

        super().save(*args, **kwargs)
class WhiteListedEmails(models.Model):
    email = models.EmailField(max_length=400, unique=True)