from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, UserRole  # Import the correct custom user model

class CustomUserAdmin(UserAdmin):
    model = UserProfile  # Use the updated UserProfile model
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'city']  # Add filters for relevant fields like 'city'
    search_fields = ['username', 'email', 'phone_number']  # Include 'phone_number' for searching
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Related Users', {'fields': ('assigned_seller', 'created_by', 'updated_by')}),  # Show related fields
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(UserProfile, CustomUserAdmin)  # Register the custom user model with the admin site
