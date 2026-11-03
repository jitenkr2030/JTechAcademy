from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'city', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'tier')
    search_fields = ('username', 'email', 'phone', 'city')
    fieldsets = UserAdmin.fieldsets + (
        ('JTech Profile', {'fields': (
            'role', 'phone', 'city', 'state', 'tier', 'avatar', 'bio',
            'specialization', 'experience_years',
        )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('JTech Profile', {'fields': (
            'role', 'phone', 'city', 'state', 'tier',
        )}),
    )
