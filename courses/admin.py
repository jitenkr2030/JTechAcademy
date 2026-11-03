from django.contrib import admin
from .models import (Programme, Course, Module, Lesson, Video,
                     Resource, LearningPathway, PathwayStep)


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'monthly_fee', 'total_fee',
                    'is_published', 'order')
    list_filter = ('is_published',)
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    ordering = ['order']


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'programme', 'is_published', 'is_self_paced',
                    'created_at')
    list_filter = ('is_published', 'is_self_paced', 'programme')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('instructors',)
    inlines = [ModuleInline, ResourceInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'lesson_count')
    list_filter = ('course__programme',)
    search_fields = ('title',)
    inlines = [LessonInline]


class VideoInline(admin.StackedInline):
    model = Video
    extra = 0


class ResourceLessonInline(admin.TabularInline):
    model = Resource
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'order',
                    'is_preview', 'is_published')
    list_filter = ('lesson_type', 'is_preview', 'is_published',
                   'module__course__programme')
    search_fields = ('title', 'description')
    inlines = [VideoInline, ResourceLessonInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'has_hd', 'has_sd', 'duration_seconds')
    list_filter = ('lesson__module__course__programme',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'lesson', 'module', 'course')
    list_filter = ('file_type',)


class PathwayStepInline(admin.TabularInline):
    model = PathwayStep
    extra = 1
    ordering = ['order']


@admin.register(LearningPathway)
class PathwayAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_months', 'total_fee',
                    'is_published', 'order')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PathwayStepInline]
