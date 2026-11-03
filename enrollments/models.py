"""
Enrollment & Subscription logic for JTech LMS.

Business rules (per JTech requirements):
- Fees are strictly monthly.
- A student can enrol for the complete course duration (full upfront)
  OR pay month-by-month (auto-recurring).
- 3-day grace period after subscription due date before access is suspended.
- Suspended students can resume by paying the overdue month.
- Completion → certificate auto-generated.
"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from courses.models import Course


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        GRACE = 'grace', 'Grace Period'
        SUSPENDED = 'suspended', 'Suspended (Payment Overdue)'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentMode(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly Auto-recurring'
        FULL = 'full', 'Full Course Fee (One-time)'

    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='enrollments')
    status = models.CharField(max_length=20, choices=Status.choices,
                              default=Status.ACTIVE)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices,
                                    default=PaymentMode.MONTHLY)

    enrolled_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Subscription cycle
    current_period_start = models.DateField(default=timezone.now)
    current_period_end = models.DateField(null=True, blank=True)
    next_billing_date = models.DateField(null=True, blank=True)

    # Razorpay IDs (filled in when payment gateway is integrated)
    razorpay_subscription_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def save(self, *args, **kwargs):
        # Initialize subscription cycle on first save
        if not self.current_period_end and self.course.programme:
            self.current_period_end = (
                self.current_period_start +
                timedelta(days=30 * self.course.programme.duration_months)
            )
            if self.payment_mode == self.PaymentMode.MONTHLY:
                self.next_billing_date = (
                    self.current_period_start + timedelta(days=30)
                )
            else:
                self.next_billing_date = None
        super().save(*args, **kwargs)

    @property
    def monthly_fee(self):
        return self.course.programme.monthly_fee

    @property
    def total_fee(self):
        return self.course.programme.total_fee

    @property
    def is_active(self):
        return self.status in (self.Status.ACTIVE, self.Status.GRACE)

    @property
    def can_access_content(self):
        return self.is_active or self.status == self.Status.COMPLETED

    def days_until_billing(self):
        if not self.next_billing_date:
            return None
        return (self.next_billing_date - timezone.now().date()).days

    def mark_completed(self):
        if self.status != self.Status.COMPLETED:
            self.status = self.Status.COMPLETED
            self.completed_at = timezone.now()
            self.save(update_fields=['status', 'completed_at'])

    def __str__(self):
        return f"{self.student} → {self.course.title} ({self.get_status_display()})"


class Payment(models.Model):
    """Record of each monthly (or one-time) payment."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE,
                                   related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    paid_at = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=30, default='razorpay')
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='success',
        choices=[('success', 'Success'), ('failed', 'Failed'),
                 ('pending', 'Pending'), ('refunded', 'Refunded')])
    invoice_url = models.URLField(blank=True)

    def __str__(self):
        return f"₹{self.amount} for {self.enrollment} on {self.paid_at.date()}"
