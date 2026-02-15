from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    list_filter = ('created_on',)
    