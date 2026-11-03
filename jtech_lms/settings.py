"""
Django settings for JTech Professional Learning Centre LMS.
Production-ready config with dev defaults. See DEPLOYMENT.md for production hardening.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: change in production
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-jtech-lms-dev-key-change-in-production-9a7f3c2b1e'
)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']  # tighten in production

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # 3rd party
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',

    # Local
    'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
    'enrollments.apps.EnrollmentsConfig',
    'progress.apps.ProgressConfig',
    'instructors.apps.InstructorsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jtech_lms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_enrollments',
            ],
        },
    },
]

WSGI_APPLICATION = 'jtech_lms.wsgi.application'
ASGI_APPLICATION = 'jtech_lms.asgi.application'

# Database — SQLite for dev; PostgreSQL for production (see DEPLOYMENT.md)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production Postgres example (uncomment + set env vars)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'jtech_lms'),
#         'USER': os.environ.get('DB_USER', 'jtech'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#         'CONN_MAX_AGE': 60,  # persistent connections — important for 10k users
#     }
# }

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'student_dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Email (dev: console; prod: SMTP / SendGrid / AWS SES)
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Caching — Redis (production), in-memory (dev)
CACHES = {
    'default': {
        'BACKEND': os.environ.get(
            'CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'
        ),
        'LOCATION': os.environ.get('REDIS_URL', 'jtech-lms-dev'),
    }
}

# Session engine — Redis-backed for 10k users in production
SESSION_ENGINE = os.environ.get(
    'SESSION_ENGINE', 'django.contrib.sessions.backends.db'
)

# File upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 524_288_000  # 500MB for video uploads (instructor)
FILE_UPLOAD_MAX_MEMORY_SIZE = 524_288_000

# JTech LMS business config
JTTECH_CONFIG = {
    'BRAND_NAME': 'JTech Professional Learning Centre',
    'SUPPORT_EMAIL': 'support@jtechlearning.in',
    'SUPPORT_PHONE': '+91-XXXXX-XXXXX',
    'CURRENCY': 'INR',
    'CURRENCY_SYMBOL': '₹',
    'LATE_FEE_GRACE_DAYS': 3,        # grace period before subscription suspends
    'CERTIFICATE_VERIFY_BASE': 'https://verify.jtechlearning.in',
}

# Razorpay keys — set via env in production
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '')
