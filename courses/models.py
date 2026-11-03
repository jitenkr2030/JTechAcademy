"""
Course models: Programme, Course, Module, Lesson, Video (HD/SD dual quality),
Resource, LearningPathway, PathwayStep.

Design supports:
- 11 JTech courses with modules + lessons
- Dual-bandwidth video (HD for Tier-1, SD/Low for Tier-2/3)
- 6 recommended learning pathways
- Per-course resources (PDFs, code samples, exercises)
"""
import os
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class Programme(models.Model):
    """Top-level grouping (e.g. 'Spoken English', 'Python Programming').
    Carries the official JTech pricing & duration."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    duration_months = models.PositiveIntegerField()
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2)
    icon = models.CharField(max_length=50, default='graduation-cap',
                            help_text="FontAwesome icon name")
    color = models.CharField(max_length=20, default='#2563eb',
                             help_text="Brand colour for cards")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    @property
    def total_fee(self):
        return self.monthly_fee * self.duration_months

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    """A specific instance of a programme — created per cohort/batch or
    one ongoing self-paced course. For JTech we use one self-paced course
    per programme."""
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE,
                                  related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    prerequisites = models.TextField(blank=True,
        help_text="What students should know before starting")
    learning_outcomes = models.TextField(blank=True,
        help_text="Bullet list, one per line")
    target_audience = models.CharField(max_length=300, blank=True)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='taught_courses',
                                         limit_choices_to={'role': 'instructor'},
                                         blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbs/', blank=True, null=True)
    intro_video_url = models.URLField(blank=True,
        help_text="YouTube or Vimeo URL for course preview")
    is_published = models.BooleanField(default=True)
    is_self_paced = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['programme__order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_duration_minutes(self):
        from django.db.models import Sum
        result = Lesson.objects.filter(module__course=self).aggregate(
            total=Sum('duration_minutes')
        )
        return result['total'] or 0

    def next_lesson_for(self, enrollment):
        """Return the next un-completed lesson for an enrollment."""
        completed_ids = set(
            enrollment.lesson_progress.filter(completed=True)
            .values_list('lesson_id', flat=True)
        )
        for module in self.modules.all():
            for lesson in module.lessons.all():
                if lesson.id not in completed_ids:
                    return lesson
        return None

    def __str__(self):
        return self.title


class Module(models.Model):
    """A module = a week or a topic within a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('course', 'order')

    @property
    def lesson_count(self):
        return self.lessons.count()

    def __str__(self):
        return f"{self.course.title} → {self.title}"


class Lesson(models.Model):
    """A single lesson — typically one video + resources + exercises."""

    class LessonType(models.TextChoices):
        VIDEO = 'video', 'Video Lesson'
        READING = 'reading', 'Reading Material'
        LIVE = 'live', 'Live Class'
        ASSIGNMENT = 'assignment', 'Assignment'
        QUIZ = 'quiz', 'Quiz'

    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                               related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    lesson_type = models.CharField(
        max_length=20, choices=LessonType.choices, default=LessonType.VIDEO
    )
    description = models.TextField(blank=True)
    content = models.TextField(blank=True,
        help_text="Markdown-friendly text content for reading lessons")
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False,
        help_text="Free preview lesson (visible without enrollment)")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Live class fields
    live_class_url = models.URLField(blank=True,
        help_text="Zoom / Google Meet / YouTube Live link")
    live_class_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.title} → {self.title}"


class Video(models.Model):
    """
    Dual-quality video asset for a lesson.
    HD version (1080p) for Tier-1 students with good bandwidth.
    SD version (480p) for Tier-2/3 students — also downloadable for offline.
    """
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE,
                                  related_name='video')
    # HD (1080p / Tier-1)
    hd_url = models.URLField(blank=True,
        help_text="HD streaming URL (HLS / direct mp4 / YouTube)")
    hd_file = models.FileField(upload_to='videos/hd/', blank=True, null=True)
    # SD (480p / Tier-2/3)
    sd_url = models.URLField(blank=True,
        help_text="Low-bandwidth streaming URL")
    sd_file = models.FileField(upload_to='videos/sd/', blank=True, null=True,
        help_text="480p file — also offered as download for offline study")
    # Optional captions (English + regional)
    captions_en = models.FileField(upload_to='captions/', blank=True, null=True)
    captions_hi = models.FileField(upload_to='captions/', blank=True, null=True)
    # Poster image
    poster = models.ImageField(upload_to='video_posters/', blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    @property
    def hd_source(self):
        return self.hd_url or (self.hd_file.url if self.hd_file else '')

    @property
    def sd_source(self):
        return self.sd_url or (self.sd_file.url if self.sd_file else '')

    @property
    def has_hd(self):
        return bool(self.hd_source)

    @property
    def has_sd(self):
        return bool(self.sd_source)

    def __str__(self):
        return f"Video for {self.lesson.title}"


class Resource(models.Model):
    """Attached downloadable resources (PDF, code, datasets, exercises)."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name='resources', blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                               related_name='resources', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='resources', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    file_type = models.CharField(max_length=20, default='pdf')

    def __str__(self):
        return self.title


class LearningPathway(models.Model):
    """
    Pre-defined combinations of courses (the 6 recommended pathways).
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    badge_color = models.CharField(max_length=20, default='#7c3aed')
    icon = models.CharField(max_length=50, default='route')
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def total_fee(self):
        return sum(step.programme.total_fee for step in self.steps.all())

    @property
    def total_months(self):
        return sum(step.programme.duration_months for step in self.steps.all())

    def __str__(self):
        return self.name


class PathwayStep(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE,
                                related_name='steps')
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ('pathway', 'order')

    def __str__(self):
        return f"{self.pathway.name} #{self.order}: {self.programme.name}"
