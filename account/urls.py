from .views import MyTokenObtainPairView, RegisterView, UserDeleteView,SuperAdminRegisterView,UpdateGetUserView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/login/", MyTokenObtainPairView.as_view(), name="Obtain_Token"),
    path("user/token/refresh", TokenRefreshView.as_view(), name="Refresh_Token"),
    path("user/register/", RegisterView.as_view(), name="Register_User"),
    path("user/<int:id>/delete/", UserDeleteView.as_view(), name="delete-user"),
    path("user/register/superadmin/", SuperAdminRegisterView.as_view(), name="Register_SuperAdmin"),
    path("user/profile/", UpdateGetUserView.as_view(), name="user-me"),
]
