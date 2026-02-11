from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/login/", views.MyTokenObtainPairView.as_view(), name="Obtain_Token"),
    path("user/token/refresh", TokenRefreshView.as_view(), name="Refresh_Token"),
    path("user/register/", views.RegisterView.as_view(), name="Register_User"),
    path("user/<str:email>/delete/", views.UserDeleteView.as_view(), name="delete-user"),
    path("user/register/superadmin/", views.SuperAdminRegisterView.as_view(), name="Register_SuperAdmin"),
    path("user/profile/", views.UpdateGetUserView.as_view(), name="user-me"),
    path("whitelist/email/",views.CreateWhiteListedEmails.as_view(),name="whitelist-create"),
    path("whitelist/<str:email>/delete/",views.WhiteListedEmailDelete.as_view(),name="whitelist-delete"),

]
