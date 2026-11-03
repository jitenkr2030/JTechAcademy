"""
Lesson player + progress tracking + certificate endpoints.

POST /learn/lesson/<id>/mark-complete/  — marks lesson done, auto-issues
certificate when all lessons of the course are done.
POST /learn/lesson/<id>/save-position/  — saves video resume position
                                       (JSON: {position, watch_percent})
"""
import json
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from courses.models import Lesson
from enrollments.models import Enrollment
from .models import LessonProgress, Certificate


@login_required
def lesson_player(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, is_published=True)
    course = lesson.module.course

    # Must be enrolled (or it's a preview)
    enrollment = None
    if not lesson.is_preview:
        enrollment = Enrollment.objects.filter(
            student=request.user, course=course
        ).first()
        if not enrollment or not enrollment.can_access_content:
            messages.error(request, "You need an active enrollment to view this lesson.")
            return redirect('course_detail', slug=course.slug)

    # Get or create progress record
    progress = None
    if enrollment:
        progress, _ = LessonProgress.objects.get_or_create(
            enrollment=enrollment, lesson=lesson
        )
        if not progress.started_at:
            progress.started_at = timezone.now()
            progress.save(update_fields=['started_at'])

    # Pick default video quality based on user tier
    user_tier = request.user.tier if request.user.is_authenticated else 'tier1'

    # Next & prev lessons in same course (for player navigation)
    all_lessons = list(Lesson.objects.filter(
        module__course=course, is_published=True
    ).order_by('module__order', 'order'))
    try:
        idx = all_lessons.index(lesson)
    except ValueError:
        idx = -1
    prev_lesson = all_lessons[idx - 1] if idx > 0 else None
    next_lesson = all_lessons[idx + 1] if 0 <= idx < len(all_lessons) - 1 else None

    return render(request, 'learn/player.html', {
        'lesson': lesson,
        'course': course,
        'module': lesson.module,
        'enrollment': enrollment,
        'progress': progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'user_tier': user_tier,
        'all_lessons': all_lessons,
        'completed_ids': set(
            enrollment.lesson_progress.filter(completed=True)
            .values_list('lesson_id', flat=True)
        ) if enrollment else set(),
    })


@require_POST
@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment,
        student=request.user, course=lesson.module.course)

    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment, lesson=lesson
    )
    progress.mark_complete()

    # Auto-complete enrollment + issue certificate if all lessons done
    total = lesson.module.course.total_lessons
    done = enrollment.lesson_progress.filter(completed=True).count()
    if total > 0 and done >= total and enrollment.status != Enrollment.Status.COMPLETED:
        enrollment.mark_completed()
        # Issue certificate
        cert, created = Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={
                'student_name': enrollment.student.display_name,
                'course_title': enrollment.course.title,
                'programme_name': enrollment.course.programme.name,
                'programme_duration': enrollment.course.programme.duration_months,
            }
        )
        messages.success(request,
            "🎉 Course complete! Your certificate has been issued.")
        return JsonResponse({
            'status': 'completed',
            'certificate_url': f"/learn/certificate/{cert.certificate_id}/"
        })

    return JsonResponse({'status': 'ok', 'completed': done, 'total': total})


@require_POST
@login_required
def save_position(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment,
        student=request.user, course=lesson.module.course)
    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment, lesson=lesson
    )

    try:
        data = json.loads(request.body)
        position = int(data.get('position', 0))
        watch_percent = min(100, max(0, int(data.get('watch_percent', 0))))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'invalid payload'}, status=400)

    progress.last_position_seconds = position
    progress.watch_percent = watch_percent
    if watch_percent >= 90 and not progress.completed:
        progress.mark_complete()
    progress.save()

    return JsonResponse({'status': 'saved', 'position': position,
                         'watch_percent': watch_percent,
                         'auto_completed': watch_percent >= 90})


def view_certificate(request, certificate_id):
    """Public certificate verification page (no login required)."""
    from django.shortcuts import get_object_or_404 as _g
    cert = _g(Certificate, certificate_id=certificate_id)
    return render(request, 'learn/certificate.html', {'cert': cert})


@login_required
def download_certificate(request, enrollment_id):
    """Stub: in production, generate a PDF certificate using ReportLab."""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id,
                                   student=request.user)
    if not hasattr(enrollment, 'certificate'):
        return HttpResponse("Certificate not yet issued.", status=404)
    cert = enrollment.certificate
    # TODO: produce actual PDF
    return HttpResponse(
        f"Certificate PDF for {cert.student_name} — {cert.course_title}\n"
        f"Verify at: {cert.verification_url}",
        content_type='text/plain'
    )
