from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

# No app_name — these are referenced un-namespaced from settings.LOGIN_URL etc.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register/instructor/', views.register_instructor, name='register_instructor'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('switch-quality/', views.switch_quality, name='switch_quality'),
]
