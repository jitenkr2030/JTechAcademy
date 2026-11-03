from django.urls import path
from . import views

app_name = 'instructors'

urlpatterns = [
    path('', views.instructor_dashboard, name='instructor_dashboard'),
    path('course/<int:course_id>/', views.course_overview, name='course_overview'),
    path('course/<int:course_id>/module/new/', views.module_create, name='module_create'),
    path('module/<int:module_id>/lesson/new/', views.lesson_create, name='lesson_create'),
    path('lesson/<int:lesson_id>/video/', views.video_attach, name='video_attach'),
    path('course/<int:course_id>/students/', views.student_progress, name='student_progress'),
]
