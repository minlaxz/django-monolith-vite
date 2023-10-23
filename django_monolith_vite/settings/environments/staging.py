from django_monolith_vite.settings.components.common import BASE_DIR
# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "django_monolith_vite-db.sqlite",
    }
}
DATABASES["default"]["CONN_MAX_AGE"] = 0

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

from django_monolith_vite.settings.components.common import TIME_ZONE

# Celery and beat configuration
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
#

# Django health check
REDIS_URL = "redis://localhost:6379"

# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches
AXES_CACHE = "default"

DJANGO_VITE_DEV_MODE = 0
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend" / "_dist"