"""
Instructor app — content creation dashboard.
Instructors can create/edit modules, lessons, upload videos (HD+SD),
attach resources, view student progress.
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib import messages

from accounts.models import User
from courses.models import Course, Module, Lesson, Video, Resource
from enrollments.models import Enrollment
from progress.models import LessonProgress

app_name = 'instructors'

def is_instructor(user):
    return user.is_authenticated and (user.is_instructor or user.is_staff)


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('title', 'description', 'order')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'lesson_type', 'description', 'content',
                  'order', 'duration_minutes', 'is_preview',
                  'is_published', 'live_class_url', 'live_class_at')


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('hd_url', 'hd_file', 'sd_url', 'sd_file',
                  'captions_en', 'captions_hi', 'poster',
                  'duration_seconds')
        labels = {
            'hd_url': 'HD Streaming URL (1080p — Tier-1)',
            'hd_file': 'Or Upload HD File',
            'sd_url': 'Low-bandwidth URL (480p — Tier-2/3)',
            'sd_file': 'Or Upload SD File (also downloadable for offline)',
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('title', 'description', 'file', 'external_url', 'file_type')


@login_required
@user_passes_test(is_instructor)
def instructor_dashboard(request):
    courses = Course.objects.filter(instructors=request.user)
    student_count = Enrollment.objects.filter(
        course__in=courses
    ).values('student').distinct().count()
    total_enrollments = Enrollment.objects.filter(course__in=courses).count()
    return render(request, 'instructors/dashboard.html', {
        'courses': courses,
        'student_count': student_count,
        'total_enrollments': total_enrollments,
    })


@login_required
@user_passes_test(is_instructor)
def course_overview(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructors=request.user)
    modules = course.modules.all().prefetch_related('lessons')
    enrollments = course.enrollments.all()
    return render(request, 'instructors/course_overview.html', {
        'course': course, 'modules': modules, 'enrollments': enrollments,
    })


@login_required
@user_passes_test(is_instructor)
def module_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructors=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f"Module '{module.title}' created.")
            return redirect('instructors:course_overview', course_id=course.id)
    else:
        form = ModuleForm(initial={'order': course.modules.count()})
    return render(request, 'instructors/form.html', {
        'form': form, 'title': f"Add Module to {course.title}",
        'course': course
    })


@login_required
@user_passes_test(is_instructor)
def lesson_create(request, module_id):
    module = get_object_or_404(Module, id=module_id,
                               course__instructors=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, f"Lesson '{lesson.title}' created.")
            return redirect('instructors:video_attach', lesson_id=lesson.id)
    else:
        form = LessonForm(initial={'order': module.lessons.count()})
    return render(request, 'instructors/form.html', {
        'form': form, 'title': f"Add Lesson to {module.title}",
        'module': module,
    })


@login_required
@user_passes_test(is_instructor)
def video_attach(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id,
                               module__course__instructors=request.user)
    video, created = Video.objects.get_or_create(lesson=lesson)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request,
                "Video saved. Both HD and Low-bandwidth versions stored.")
            return redirect('instructors:course_overview',
                            course_id=lesson.module.course.id)
    else:
        form = VideoForm(instance=video)
    return render(request, 'instructors/video_form.html', {
        'form': form, 'lesson': lesson,
        'title': f"Attach Video to {lesson.title}"
    })


@login_required
@user_passes_test(is_instructor)
def student_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructors=request.user)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    rows = []
    for e in enrollments:
        total = course.total_lessons
        done = e.lesson_progress.filter(completed=True).count()
        pct = (done / total * 100) if total else 0
        rows.append({'enrollment': e, 'done': done, 'total': total,
                     'pct': round(pct, 1)})
    return render(request, 'instructors/student_progress.html', {
        'course': course, 'rows': rows
    })
