"""
Django settings for galela_solutions_backend.

Reads secrets and environment-specific values from .env
so nothing sensitive lives in source control.
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

# ── Load .env ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


# ── Security ──────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-unsafe-key-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]


# ── Applications ──────────────────────────────────────────────
INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

     # Local apps
    'apps.catalog',
    'apps.requests',
    'apps.analytics',
    'apps.dashboard',

]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',      # ← must be near the top
    'django.middleware.security.SecurityMiddleware',
      'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'galela_solutions_backend.urls'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ── Templates ─────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ── WSGI / ASGI ───────────────────────────────────────────────
WSGI_APPLICATION = 'galela_solutions_backend.wsgi.application'
ASGI_APPLICATION = 'galela_solutions_backend.asgi.application'


# ── Database — Postgres (Docker locally, Supabase in prod) ────
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{os.getenv('DB_USER', 'galela')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'Galela_Solutions')}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ── Password validation ───────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Analytics ─────────────────────────────────────────────
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN', '')

# ── Dashboard ────────────────────────────────────────────────
DASHBOARD_KEY = os.getenv('DASHBOARD_KEY', '')


# ── Internationalisation ──────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Johannesburg'    # ← your local timezone
USE_I18N = True
USE_TZ = True


# ── Static files ──────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ── Default primary key type ──────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Django REST Framework ─────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',   # we'll tighten per-view
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# ── CORS ──────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    if o.strip()
]
CORS_ALLOW_CREDENTIALS = True