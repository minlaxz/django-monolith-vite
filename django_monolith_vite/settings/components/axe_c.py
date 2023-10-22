"""
Axes is temporarily disabled
django-axes==5.27.0
"""

from django_monolith_vite.settings.components.auth import AUTHENTICATION_BACKENDS
from django_monolith_vite.settings.components.common import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += (
    # Security
    "axes"
)

AUTHENTICATION_BACKENDS += (
    "axes.backends.AxesBackend",
)

MIDDLEWARE += (
    # Axes:
    "axes.middleware.AxesMiddleware",
)

# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches
AXES_CACHE = "default"
