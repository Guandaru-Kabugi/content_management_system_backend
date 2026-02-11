from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,WhiteListedEmails

# Register your models here.
@admin.register(WhiteListedEmails)
class WhiteListedEmailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('email')
    }))
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id','role','username', 'full_name', 'email', 'image_url']
     # Add your custom fields to the detail/edit page
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'full_name', 'role', 'image_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
     # Optional: include fields when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'image_url', 'password1', 'password2'),
        }),
    )