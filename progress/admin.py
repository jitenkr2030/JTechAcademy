from django.contrib import admin
from .models import LessonProgress, Certificate


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'watch_percent',
                    'completed_at')
    list_filter = ('completed',)
    search_fields = ('enrollment__student__username', 'lesson__title')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'student_name', 'course_title',
                    'programme_name', 'issued_at')
    search_fields = ('student_name', 'course_title', 'certificate_id')
    readonly_fields = ('certificate_id', 'verification_url', 'issued_at')
