from .base import *
from decouple import Csv


DEBUG = True
ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# Environments
ENVIRONMENT = 'TESTING'
