# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
'''


from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='ve#3*k+er8q=*lk5(4*$qmjjm6oam@!#=o#u4(h0l79#q!0tqk')

# Mail settings
# ------------------------------------------------------------------------------
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
#                     default='django.core.mail.backends.console.EmailBackend')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', 'corsheaders',)

SECURITY_MIDDLEWARE = (
    'djangosecure.middleware.SecurityMiddleware',
)

CORS_MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
)

MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + CORS_MIDDLEWARE + MIDDLEWARE_CLASSES

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CELERY_ALWAYS_EAGER = True

# Your local stuff: Below this line define 3rd party library settings
FILE_UPLOAD_PREFIX_FOLDER_USER = 'user'

TASTYPIE_FULL_DEBUG = True
