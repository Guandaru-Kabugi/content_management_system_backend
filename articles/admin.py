from django.contrib import admin
from .models import Article

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'external_url', 'thumbnail_url', 'status', 'visibility', 'recent_or_old']
    list_filter = ('recent_or_old', 'status', 'visibility')
    