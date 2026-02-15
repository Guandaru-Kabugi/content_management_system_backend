from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Notification(models.Model):
    ACTION_CHOICES = (
        ("created", "Created"),
        ("updated", "Updated"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='created')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title