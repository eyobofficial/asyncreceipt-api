import os
from decouple import config, Csv
from environ import Path


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__) - 3


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# Third Party apps
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',
    'drf_yasg',
]


# Project apps
INSTALLED_APPS += [
    'accounts.apps.AccountsConfig',
    'receipts.apps.ReceiptsConfig',
]


# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


#  POSTRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('RDS_DB_NAME'),
        'USER': config('RDS_USERNAME'),
        'PASSWORD': config('RDS_PASSWORD'),
        'HOST': config('RDS_HOSTNAME'),
        'PORT': config('RDS_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Addis_Ababa'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Sites Framework
SITE_ID = 1


# Static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Custom Auth User Model
AUTH_USER_MODEL = 'accounts.CustomUser'


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# Cors Headers
CORS_ORIGIN_ALLOW_ALL = True


# Default Admin Account
DEFAULT_ADMIN_USERNAME = config('ADMIN_USERNAME')
DEFAULT_ADMIN_EMAIL = config('ADMIN_EMAIL')
DEFAULT_ADMIN_PASSWORD = config('ADMIN_PASSWORD')
DEFAULT_ADMIN_FIRST_NAME = config('ADMIN_FIRST_NAME', '')
DEFAULT_ADMIN_LAST_NAME = config('ADMIN_LAST_NAME', '')


# Project Name
PROJECT_NAME = 'Receipt API'


# Celery
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    )
}


# Swagger
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Token': {
            'type': 'key',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}
