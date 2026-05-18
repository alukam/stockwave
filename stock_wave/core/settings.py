import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-89g+fpe-@$atc%6%+_h0w1d$5yqw)v5mdmfo@ts3p9by!3-hnx')

# FIXED: Dynamically flip DEBUG to False on Render so errors don't leak, default to True locally
DEBUG = 'RENDER' not in os.environ

# ALLOWED HOSTS
ALLOWED_HOSTS = ['*'] 

# --- APPS ---
INSTALLED_APPS = [
    'categories',
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
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}
'''''''''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory_db',
        'USER': 'inventory_users',      # usually 'postgres'
        'PASSWORD': '2000@2000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
'''''



# If we are on Render, force SSL connection parameters for Postgres
if 'RENDER' in os.environ:
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' 

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- AUTHENTICATION ROUTING (FIXED DUPLICATES) ---
# We use explicit string names that match your path('...', name='...') configs
LOGIN_URL = 'login'          
LOGIN_REDIRECT_URL = 'dashboard'  
LOGOUT_REDIRECT_URL = 'login'     

# --- MISC ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'