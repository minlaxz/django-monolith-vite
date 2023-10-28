from django_monolith_vite.settings.environments.staging import *
import os
# import dj_database_url

# DATABASE_URL = os.environ.get("DATABASE_URL")
# db_from_env = dj_database_url.config(
#     default=DATABASE_URL, conn_max_age=500, ssl_require=False
# )
# DATABASES["default"].update(db_from_env)

# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
        "OPTIONS": {"sslmode": "require"},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# from django_monolith_vite.settings.components.common import TIME_ZONE

# Celery and beat configuration
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Django health check
# REDIS_URL = "redis://localhost:6379"

# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches
# AXES_CACHE = "default"
