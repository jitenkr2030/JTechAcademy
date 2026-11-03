from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('<int:course_id>/', views.enroll, name='enroll'),
    path('<int:enrollment_id>/cancel/', views.cancel, name='cancel'),
    path('<int:enrollment_id>/pay/', views.pay_now, name='pay_now'),
    path('my/', views.my_enrollments, name='my_enrollments'),
    path('success/<int:enrollment_id>/', views.enrollment_success,
         name='enrollment_success'),
]
