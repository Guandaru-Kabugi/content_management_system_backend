from django.urls import path
from . import views

urlpatterns =[
    path("notifications/", views.CreateNotificationView.as_view(), name="createlist-notification"),
    path("notification/<int:pk>/", views.UpdateGetDeleteANotification.as_view(), name="Notification-Detail"),
]