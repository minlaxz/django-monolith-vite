"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""
import os

from django_monolith_vite.settings.components import logging
from django_monolith_vite.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
    TIME_ZONE,
)


INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # https://github.com/bradmontgomery/django-querycount
    "querycount.middleware.QueryCountMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
)

# Can add third party panels here
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


def _custom_show_toolbar(request) -> bool:  # noqa: C901
    """Only show the debug toolbar to users with the superuser flag."""
    # This file will not be picked up by `__init__.py`
    # so we don't need to check STG_DEBUG
    return bool(os.environ.get("DEBUG", False))


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": (
        "django_monolith_vite.settings.environments.development._custom_show_toolbar"
    ),
}
EXTRA_SIGNALS = ["allauth.socialaccount.signals"]
INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "django_monolith_vite-db.sqlite",
    }
}
DATABASES["default"]["CONN_MAX_AGE"] = 0
#

# Email configuration
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_HOST_USER = "minminlaxz@gmail.com"
DEFAULT_FROM_EMAIL = "minlaxz.io <minminlaxz@gmail.com>"
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
SENDGRID_SANDBOX_MODE_IN_DEBUG = True
SENDGRID_ECHO_TO_STDOUT = True
#

# Development Config: query count.
QUERYCOUNT = {
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 0,
    },
    "IGNORE_REQUEST_PATTERNS": [r"^/admin/", r"^/app/", r"^/static/"],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": None,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}

# Celery and beat configuration
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
#


# Recptcha configuration
RECAPTCHA_REQUIRED_SCORE = 0.5
# For V3
RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]

# Django health check
REDIS_URL = "redis://localhost:6379"

# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#     },
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches
AXES_CACHE = "default"


# Need by slack => no trailing slash needed
APP_DOMAIN = "https://localhost:8000"
SLACK_CALLBACK = APP_DOMAIN


# logging settings
# LOGGING = {**logging.LOGGING}

# Django-Vite use HMR or not.
DJANGO_VITE_DEV_MODE = bool(int(os.environ.get("DJANGO_VITE_DEV_MODE", 1)))



print("LOG: Development settings file is loaded.")
