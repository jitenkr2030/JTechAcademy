from django.urls import path
from . import views

# No app_name — these are top-level public URLs (home, courses/, pathways/, about/)
urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('pathways/', views.pathway_list, name='pathway_list'),
    path('pathways/<slug:slug>/', views.pathway_detail, name='pathway_detail'),
    path('about/', views.about, name='about'),
]
