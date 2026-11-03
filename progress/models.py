"""
Progress tracking & certificate generation.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from courses.models import Lesson
from enrollments.models import Enrollment


class LessonProgress(models.Model):
    """Tracks whether a student has completed a lesson, plus watch percentage."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE,
                                   related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name='progress_records')
    completed = models.BooleanField(default=False)
    watch_percent = models.PositiveIntegerField(default=0,
        help_text="0-100, how much of the video has been watched")
    last_position_seconds = models.PositiveIntegerField(default=0,
        help_text="Resume position for video")
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')
        ordering = ['lesson__order']

    def mark_complete(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=['completed', 'completed_at', 'updated_at'])

    def __str__(self):
        return f"{self.enrollment.student} → {self.lesson.title} " \
               f"({'✓' if self.completed else '...'})"


class Certificate(models.Model):
    """Auto-generated upon course completion. Verifiable via UUID."""
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE,
                                      related_name='certificate')
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False,
                                      unique=True)
    issued_at = models.DateTimeField(default=timezone.now)
    student_name = models.CharField(max_length=300)
    course_title = models.CharField(max_length=300)
    programme_name = models.CharField(max_length=300)
    programme_duration = models.PositiveIntegerField()
    grade = models.CharField(max_length=10, default='Pass',
        help_text="Pass / Distinction / specific grade")
    verification_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.verification_url:
            base = settings.JTTECH_CONFIG.get('CERTIFICATE_VERIFY_BASE',
                                              'https://verify.jtechlearning.in')
            self.verification_url = f"{base}/verify/{self.certificate_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate {self.certificate_id} — {self.student_name}"
