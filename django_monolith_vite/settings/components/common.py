import os
import structlog

from pathlib import Path
from typing import Tuple

logger = structlog.get_logger(__name__)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.environ.get("DEBUG") or os.environ.get("STG_DEBUG") or False == "True"
SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("STG_SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",") or os.environ.get(
    "STG_ALLOWED_HOSTS"
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en", "English"),
    ("ja", "Japanese"),
]
TIME_ZONE = "Asia/Yangon"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale/"),
]

INSTALLED_APPS: Tuple[str, ...] = (
    # Built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third-parties
    # "rest_framework",
    "captcha",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_vite",
    "guardian",
    "django_fsm",
    "django_extensions",
    # Local Apps,
    "dmv_home",
    "frontend",
    "api",
)

MIDDLEWARE: Tuple[str, ...] = (
    # Logging:
    "django_monolith_vite.settings.components.middlewares.LoggingContextVarsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # django-permissions-policy
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Django HTTP Referrer Policy:
    "django_http_referrer_policy.middleware.ReferrerPolicyMiddleware",
    "allauth.account.middleware.AccountMiddleware",
)

# [DISABLED APPS]
DISABLED_APPS = []
SETTINGS_EXPORT = ["DISABLED_APPS"]

ROOT_URLCONF = "django_monolith_vite.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_monolith_vite.wsgi.application"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = "/media/"  # Public URL at the browser
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")


STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
    os.path.join(BASE_DIR, "frontend/_dist/"),
)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# [END staticurl]

# [CUSTOM APP Settings]
PERSONAL_PREFIX = "p-"
VERIFICATION_EXPIRE_DAY = 3
LEAST_WORD_TOKENS = 20
MAX_PROFILE_IMAGE_SIZE = 1.0 * 1024 * 1024  # 1MB
MAX_ASSERT_IMAGE_SIZE = 3.0 * 1024 * 1024  # 3MB
MAX_ATTACHMENT_SIZE = 5.0 * 1024 * 1024  # 5MB
MAX_VERIFICATION_COUNTER = 3
MAX_VERIFICATION_COOLDOWN = 10 * 60  # 10 minutes


# Guardian init
ANONYMOUS_USER_NAME = None

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT
EMAIL_TIMEOUT = 5

# Vite
# Where ViteJS assets are built.
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend" / "_dist"

logger.info("LOG: common settings module is loaded.")
