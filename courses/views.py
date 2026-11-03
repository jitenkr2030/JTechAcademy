"""
Course catalog views: home, course list, course detail, pathways.
"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Programme, Course, Module, Lesson, LearningPathway


def home(request):
    programmes = Programme.objects.filter(is_published=True)
    pathways = LearningPathway.objects.filter(is_published=True)[:6]
    featured = Course.objects.filter(is_published=True)[:3]
    return render(request, 'home.html', {
        'programmes': programmes,
        'pathways': pathways,
        'featured': featured,
    })


def course_list(request):
    programmes = Programme.objects.filter(is_published=True).annotate(
        course_count=Count('courses', filter=models_q('is_published'))
    )
    return render(request, 'courses/list.html', {'programmes': programmes})


def models_q(field):
    """Helper to avoid importing Q at top level if not needed."""
    from django.db.models import Q
    return Q(**{f'courses__{field}': True})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.all().prefetch_related('lessons')

    # If student is enrolled, pass enrollment + progress
    enrollment = None
    completed_lesson_ids = set()
    if request.user.is_authenticated and request.user.is_student:
        enrollment = course.enrollments.filter(student=request.user).first()
        if enrollment:
            completed_lesson_ids = set(
                enrollment.lesson_progress.filter(completed=True)
                .values_list('lesson_id', flat=True)
            )

    return render(request, 'courses/detail.html', {
        'course': course,
        'modules': modules,
        'enrollment': enrollment,
        'completed_lesson_ids': completed_lesson_ids,
    })


def pathway_list(request):
    pathways = LearningPathway.objects.filter(is_published=True)
    return render(request, 'courses/pathways.html', {'pathways': pathways})


def pathway_detail(request, slug):
    pathway = get_object_or_404(LearningPathway, slug=slug, is_published=True)
    steps = pathway.steps.all().select_related('programme')
    return render(request, 'courses/pathway_detail.html', {
        'pathway': pathway, 'steps': steps
    })


def about(request):
    return render(request, 'about.html')
