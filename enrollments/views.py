"""
Enrollment views.

NOTE on payments: For the demo, the "enroll" view marks the enrollment active
without going through Razorpay. In production, replace `enroll()` with a flow
that creates a Razorpay subscription/order, redirects to Razorpay Checkout,
and only activates the enrollment after the webhook confirms payment.
See DEPLOYMENT.md §"Razorpay Integration".
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from courses.models import Course
from progress.models import LessonProgress, Certificate
from .models import Enrollment, Payment


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    if not request.user.is_student:
        messages.error(request, "Only students can enrol in courses.")
        return redirect('course_detail', slug=course.slug)

    existing = Enrollment.objects.filter(student=request.user, course=course).first()
    if existing:
        messages.info(request, f"You're already enrolled in {course.title}.")
        return redirect('enrollments:enrollment_success', enrollment_id=existing.id)

    payment_mode = request.POST.get('payment_mode', Enrollment.PaymentMode.MONTHLY)
    if payment_mode not in dict(Enrollment.PaymentMode.choices):
        payment_mode = Enrollment.PaymentMode.MONTHLY

    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course,
        status=Enrollment.Status.ACTIVE,
        payment_mode=payment_mode,
        current_period_start=timezone.now().date(),
    )

    # Record the initial payment (demo; in prod this comes from Razorpay webhook)
    amount = course.programme.monthly_fee if payment_mode == Enrollment.PaymentMode.MONTHLY \
             else course.programme.total_fee
    Payment.objects.create(
        enrollment=enrollment,
        amount=amount,
        period_start=enrollment.current_period_start,
        period_end=enrollment.current_period_end or (
            enrollment.current_period_start + timedelta(days=30)
        ),
        method='demo',
        transaction_id=f'DEMO-{enrollment.id}-{int(timezone.now().timestamp())}',
        status='success',
    )

    messages.success(request, f"Enrolled successfully in {course.title}!")
    return redirect('enrollments:enrollment_success', enrollment_id=enrollment.id)


@login_required
def enrollment_success(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id,
                                   student=request.user)
    return render(request, 'enrollments/success.html', {
        'enrollment': enrollment
    })


@login_required
def cancel(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id,
                                   student=request.user)
    if request.method == 'POST':
        enrollment.status = Enrollment.Status.CANCELLED
        enrollment.save(update_fields=['status'])
        messages.info(request, "Enrollment cancelled. You'll retain access "
                                "until the current period ends.")
    return redirect('student_dashboard')


@login_required
def pay_now(request, enrollment_id):
    """Trigger a manual payment (e.g. when subscription lapsed).
    In production: create Razorpay order → redirect → webhook confirms."""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id,
                                   student=request.user)
    Payment.objects.create(
        enrollment=enrollment,
        amount=enrollment.monthly_fee,
        period_start=timezone.now().date(),
        period_end=timezone.now().date() + timedelta(days=30),
        method='demo',
        transaction_id=f'DEMO-{enrollment.id}-{int(timezone.now().timestamp())}',
        status='success',
    )
    enrollment.status = Enrollment.Status.ACTIVE
    enrollment.current_period_start = timezone.now().date()
    enrollment.next_billing_date = timezone.now().date() + timedelta(days=30)
    enrollment.save()
    messages.success(request, "Payment received. Your enrollment is active again.")
    return redirect('student_dashboard')


@login_required
def my_enrollments(request):
    if not request.user.is_student:
        return redirect('home')
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'enrollments/list.html', {'enrollments': enrollments})
