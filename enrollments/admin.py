from django.contrib import admin
from .models import Enrollment, Payment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'payment_mode',
                    'next_billing_date', 'enrolled_at')
    list_filter = ('status', 'payment_mode', 'course__programme')
    search_fields = ('student__username', 'student__email', 'course__title')
    date_hierarchy = 'enrolled_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'amount', 'period_start', 'period_end',
                    'paid_at', 'method', 'status')
    list_filter = ('status', 'method')
    date_hierarchy = 'paid_at'
