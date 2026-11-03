"""
Custom user model with roles: student / instructor / admin.
Single source of truth for auth throughout the LMS.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        INSTRUCTOR = 'instructor', 'Instructor'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.STUDENT
    )
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    tier = models.CharField(
        max_length=10,
        choices=[('tier1', 'Tier-1 (HD)'), ('tier2', 'Tier-2/3 (Low BW)')],
        default='tier1',
        help_text="Used to default video quality; user can override in player."
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    # For instructors
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"
