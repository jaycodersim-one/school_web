"""
Production settings for config project.
"""

from .settings import *
import os
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Temporarily set to True for debugging

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    'jaycodersim.pythonanywhere.com',
    'www.jaycodersim.pythonanywhere.com',
    'localhost',
    '127.0.0.1'
]

# Database
# Use MySQL on PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jaycodersim$school_web',
        'USER': 'jaycodersim',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'jaycodersim.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/home/jaycodersim/school_web/staticfiles'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/jaycodersim/school_web/media'

# Static files storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'  # Changed from whitenoise

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}