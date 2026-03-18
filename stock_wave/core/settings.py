import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
# Get secret key from environment variable, or use the insecure one for local dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-89g+fpe-@$atc%6%+_h0w1d$5yqw)v5mdmfo@ts3p9by!3-hnx')

# Debug should be False in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Render domain and localhost
ALLOWED_HOSTS = ['*'] 

# --- APPS ---
INSTALLED_APPS = [
    'debtors',
    'expenses',
    'products',
    'reports',
    'sales',
    'users',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = 'users.User'

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # REQUIRED for static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sales.context_processors.totals_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- DATABASE ---
# This looks for a DATABASE_URL environment variable (from Render). 
# If it doesn't find one, it falls back to your local PostgreSQL settings.
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://inventory_users:2000@2000@localhost:5432/inventory_db',
        conn_max_age=600
    )
}

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # Required for production

# Enable WhiteNoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- LOGINS ---
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# --- MISC ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'