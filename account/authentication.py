
from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate using either email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Trying email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Then try username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
