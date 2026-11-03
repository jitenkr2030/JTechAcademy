from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('lesson/<int:lesson_id>/', views.lesson_player, name='lesson_player'),
    path('lesson/<int:lesson_id>/mark-complete/',
         views.mark_lesson_complete, name='mark_complete'),
    path('lesson/<int:lesson_id>/save-position/',
         views.save_position, name='save_position'),
    path('certificate/<uuid:certificate_id>/',
         views.view_certificate, name='view_certificate'),
    path('certificate/<int:enrollment_id>/download/',
         views.download_certificate, name='download_certificate'),
]
