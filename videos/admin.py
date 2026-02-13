from django.contrib import admin
from .models import Tag,Videos
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on', 'updated_on']

@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ['id','creator','title', 'cloudnary_url', 'weblink_url', 'thumbnail_url', 'status', 'visibility']
    list_filter = ('creator', 'status', 'visibility')
    