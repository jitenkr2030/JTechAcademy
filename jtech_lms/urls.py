"""
URL configuration for JTech LMS.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # PWA endpoints
    path('manifest.json', TemplateView.as_view(
        template_name='pwa/manifest.json',
        content_type='application/json',
    ), name='pwa_manifest'),
    path('sw.js', TemplateView.as_view(
        template_name='pwa/sw.js',
        content_type='application/javascript',
    ), name='pwa_sw'),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='pwa_offline'),

    # App routes
    path('', include('courses.urls')),
    path('accounts/', include('accounts.urls')),
    path('enroll/', include('enrollments.urls')),
    path('learn/', include('progress.urls')),
    path('teach/', include('instructors.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
