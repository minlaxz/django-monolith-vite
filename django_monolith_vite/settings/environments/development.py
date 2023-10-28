"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""
import os

from django_monolith_vite.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
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

# Django-Vite use HMR or not.
DJANGO_VITE_DEV_MODE = 1



print("LOG: Development settings file is loaded.")
