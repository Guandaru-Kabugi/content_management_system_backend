from django.contrib import admin
from .models import Tag,Videos
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on', 'updated_on']