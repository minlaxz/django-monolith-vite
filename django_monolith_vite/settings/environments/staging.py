from django_monolith_vite.settings.components.common import BASE_DIR, MIDDLEWARE

DEBUG = False

MIDDLEWARE = list(MIDDLEWARE)
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE = tuple(MIDDLEWARE)

# https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# testing locally with no postgres container
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "django_monolith_vite-db.sqlite",
#     }
# }
# DATABASES["default"]["CONN_MAX_AGE"] = 0

DJANGO_VITE_DEV_MODE = 0
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend" / "_dist"
