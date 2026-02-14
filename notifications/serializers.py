from .models import Notification
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','user', 'title', 'content', 'created_on', 'updated_on']
        read_only_fields = ['id', 'user']