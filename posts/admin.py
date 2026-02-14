from django.contrib import admin
from .models import Post

# Register your models here.
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'date_posted', 'status', 'visibility', 'is_commentary']
    list_filter = ('date_posted', 'status', 'visibility', 'is_commentary')
    