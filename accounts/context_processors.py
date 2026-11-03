"""
Context processor exposing the current student's active enrollments
across all templates (used in navbar / dashboard).
"""
from enrollments.models import Enrollment


def user_enrollments(request):
    if not request.user.is_authenticated or not request.user.is_student:
        return {}
    active = Enrollment.objects.filter(
        student=request.user,
        status__in=['active', 'grace']
    ).select_related('course')[:6]
    return {'active_enrollments': active}
