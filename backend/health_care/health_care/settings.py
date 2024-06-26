"""
Django settings for health_care project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os, random, string, inspect
from pathlib import Path

import django_dyn_dt

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3gujp=x^o9_dho(8@rye#bc-2k-$isjrxtrje1pfs_*@90)qll"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:5085',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:5085',
    'https://tame-hornets-cheat.loca.lt'  # Agrega tu URL aquí
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'tame-hornets-cheat.loca.lt'  # Agrega tu URL aquí
]




# Application definition

INSTALLED_APPS = [  
    'admin_datta.apps.AdminDattaConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_select2",
    "django.contrib.staticfiles",
    'crispy_forms',
    #'admin_volt.apps.AdminVoltConfig',
    "drf_spectacular",
    "home",
    'django_dyn_dt',             # <-- NEW: Dynamic_DT

    # Tooling API-GEN
    'django_api_gen',            # Django API GENERATOR  # <-- NEW
    'rest_framework',            # Include DRF           # <-- NEW 
    'rest_framework.authtoken',
    # Include DRF Auth      # <-- NEW   
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "health_care.urls"

CSRF_COOKIE_NAME = 'csrftoken'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOME_TEMPLATES      = os.path.join(BASE_DIR, 'templates') 
TEMPLATE_DIR_DATATB = os.path.join(BASE_DIR, "django_dyn_dt/templates") 

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [HOME_TEMPLATES, TEMPLATE_DIR_DATATB],                  # <-- UPD: Dynamic_DT
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            'libraries': {  # Agrega esta línea para cargar la etiqueta de formulario Crispy Forms
                'crispy_forms_tags': 'crispy_forms.templatetags.crispy_forms_tags',
            },
        },
    },
]

WSGI_APPLICATION = "health_care.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'healthcare',
        'USER': 'admin_hcare',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'BOOTSTRAP_CSS_URL': '/static/css/bootstrap.min.css'
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Health Care API',
    'DESCRIPTION': 'List of all API endpoints',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'SERVE_PUBLIC': True,
    # OTHER SETTINGS
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    # None will default to DRF's AUTHENTICATION_CLASSES
    'SERVE_AUTHENTICATION': None,
    'COMPONENT_SPLIT_REQUEST': False,
    'ENFORCE_NON_BLANK_FIELDS': False,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es"

TIME_ZONE = "America/Costa_Rica"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DYN_DB_PKG_ROOT = os.path.dirname( inspect.getfile( django_dyn_dt ) ) # <-- NEW: Dynamic_DT

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(DYN_DB_PKG_ROOT, "templates/static"),                # <-- NEW: Dynamic_DT 
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
