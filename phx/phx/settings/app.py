"""
App-specific settings

Applied to all envs
"""

import os
from pathlib import Path

import environ

from ..helpers.logging import skip_404s, skip_during_testing

# app roots
django_root = environ.Path(__file__) - 3
app_root = environ.Path(django_root) - 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'easy_thumbnails',
    'nested_admin',
    'django_extensions',
    'ckeditor',
    'admin_ordering',

    # PHX
    'components.apps.ComponentsConfig',
    'contact.apps.ContactConfig',
    'fixtures.apps.FixturesConfig',
    'home.apps.HomeConfig',
    'news.apps.NewsConfig',
    'pages.apps.PagesConfig',
    'results.apps.ResultsConfig',
    'gallery.apps.GalleryConfig',
    'files.apps.FilesConfig',
    'social.apps.SocialConfig',
    'error.apps.ErrorConfig',
    'offline.apps.OfflineConfig',
    'athletes.apps.AthletesConfig',
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

ROOT_URLCONF = 'phx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(django_root.path('templates/')).resolve()],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # PHX
                'phx.context_processors.global_config.global_config',
                'phx.context_processors.nav.nav',
            ],
            'libraries': {
                'templatehelpers': 'phx.templatetags.templatehelpers',
                'highlight': 'phx.templatetags.highlight',
                'paginator': 'phx.templatetags.paginator',
            }
        },
    },
]

WSGI_APPLICATION = 'phx.wsgi.application'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'ignore_404': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_404s,
        },
        'ignore_during_testing': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_during_testing,
        },
    },
    'formatters': {
        'save_to_log_file': {
            'format': '[{asctime}] [{levelname}] ({module}): {message}',
            'style': '{',
        },
        'django_server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django_server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django_server',
        },
        'save_to_log_file': {
            'level':
            'WARNING',
            'filters': [
                'ignore_404',
                'ignore_during_testing',
                'require_debug_false',
            ],
            'class':
            'logging.handlers.RotatingFileHandler',
            'filename':
            os.path.join(app_root.path('logs'), 'phx.log'),
            'maxBytes':
            1024 * 1024 * 15,  # 15MB
            'backupCount':
            10,
            'formatter':
            'save_to_log_file',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'ignore_during_testing'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'save_to_log_file', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django_server', 'save_to_log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['django_server', 'save_to_log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'save_to_log_file', 'mail_admins'],
        'level': 'INFO',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

# Files

SITE_ROOT = django_root()

MEDIA_ROOT = app_root('media')
MEDIA_URL = '/media/'

STATIC_ROOT = app_root('static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(app_root(), 'frontend', 'static'),
]

# DB
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True

# CK Editor
# https://github.com/django-ckeditor/django-ckeditor

CKEDITOR_CONFIGS = {
    'text': {
        'toolbar': [
            ['Undo', 'Redo'],
            ['Bold', 'Italic'],
            ['Link', 'Unlink'],
            ['NumberedList', 'BulletedList'],
        ],
        'height':
        200,
        'width':
        700,
        'removeDialogTabs':
        'link:advanced;link:target',
    },
    'table': {
        'toolbar': [
            ['Undo', 'Redo'],
            ['Bold', 'Italic'],
            ['Link', 'Unlink'],
            ['Table'],
        ],
        'height':
        200,
        'width':
        700,
        'removeDialogTabs':
        'table:advanced',
    },
}

# Misc

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

FILE_UPLOAD_PERMISSIONS = 0o644

# Template values

SITE_TITLE = 'Brighton Phoenix'
SITE_DESCRIPTION = (
    'Pursuing excellence and honours in athletics and multisport, road, track '
    'and cross-country running, triathlon/duathlon. Coaching and competition, '
    'advice and inspiration – for all ages and abilities.')
