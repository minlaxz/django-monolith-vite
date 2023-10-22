"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ
import structlog
from split_settings.tools import include, optional
import sys
from . import env_injector


logger = structlog.get_logger(__name__)

_ENV = environ.get("DJANGO_ENV", "development")

if not _ENV:
    _msg = "Err: backend enviroment variable is missing!"
    logger.error(_msg)
    sys.exit(1)
else:
    logger.info(f"LOG: current environment: {_ENV}")
    if _ENV == "development":
        env_injector.update_configs_from_env()
        # env_injector.update_configs_from_vault(for_env=_ENV)
    elif _ENV == "testing":
        env_injector.update_configs_from_env()


base_settings = [
    "components/common.py",  # standard django settings
    "components/cleanhtmlfields.py",
    # "components/axe_c.py",
    "components/auth.py",  # authentications, object permissons and validations
    "components/logging.py",  # logging settings
    "components/rest.py",  # REST settings
    "components/security.py",  # security settings
    "environments/{0}.py".format(
        _ENV if _ENV != "testing" else "development"
    ),  # Our selected environment
    optional("environments/local.py"),  # Optionally override some settings:
]

# Include settings:
include(*base_settings)
