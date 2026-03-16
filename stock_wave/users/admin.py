from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # This adds our custom fields to the User List view (the table)
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    
    # This adds our custom fields to the "Edit User" page
    fieldsets = UserAdmin.fieldsets + (
        ('IMS Status', {'fields': ('role', 'is_approved', 'phone_number')}),
    )
    
    # This allows you to edit the fields when creating a user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('IMS Status', {'fields': ('role', 'is_approved', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)