# Django authentication system
# https://docs.djangoproject.com/en/3.2/topics/auth/

"""authentication configuration"""

import os
from datetime import timedelta
import structlog

logger = structlog.get_logger(__name__)

# [ALL AUTH SETTINGS : START]
ACCOUNT_ADAPTER = "dmv_home.adapters.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "dmv_home.adapters.CustomSocialAccountAdapter"
# Not using username field, we are using email field instead
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_FORMS = {
    # "login": "allauth.account.forms.LoginForm",
    # "reset_password": "allauth.account.forms.ResetPasswordForm",
    "signup": "dmv_home.forms.UserSignupForm",
    "login": "dmv_home.forms.UserLoginForm",
    "reset_password": "dmv_home.forms.UserPasswordResetForm",
}
ACCOUNT_EMAIL_REQUIRED = True  # Required by ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = (
    None  # Successful login goes to .../{{locale}}/ app
)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # 1 day
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # 'mandatory' or 'optional'
# Email Confirmation is required for all users, except for those who are already confirmed
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[minlaxz]"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 120  # wait 2 minutes
ACCOUNT_MAX_EMAIL_ADDRESSES = 1  # 1 email address
ACCOUNT_PASSWORD_MIN_LENGTH = 8  # 8 characters
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 6  # 6 attempts
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600  # 10 minutes
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True # logout all session when password is changed.
ACCOUNT_RATE_LIMITS = {
    # Change password view (for users already logged in)
    "change_password": "5/m",
    # Email management (e.g. add, remove, change primary)
    "manage_email": "10/m",
    # Request a password reset, global rate limit per IP
    "reset_password": "20/m",
    # Rate limit measured per individual email address
    "reset_password_email": "5/m",
    # Password reset (the view the password reset email links to).
    "reset_password_from_key": "20/m",
    # Signups.
    "signup": "20/m",
    # NOTE: Login is already protected via `ACCOUNT_LOGIN_ATTEMPTS_LIMIT`
}
# Other settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True


# To kick in the socail account signup form
SOCIALACCOUNT_AUTO_SIGNUP = False

SOCIALACCOUNT_FORMS = {
    "signup": "dmv_home.forms.CustomSocialSignupForm",
}
SOCIALACCOUNT_STORE_TOKENS = False

SITE_ID = 3
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("SSO_GOOGLE_CLIENT_ID", ""),
            "secret": os.environ.get("SSO_GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",  # Login with SSO
    "dmv_home.backends.EmailAuthenticationBackend",  # Login with email as username
    "guardian.backends.ObjectPermissionBackend",  # Object permission
    # 'django.contrib.auth.backends.ModelBackend', # this is default
)

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "knox.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": 10,
    "AUTO_REFRESH": True,
    "EXPIRY_DATETIME_FORMAT": "ISO_8601",
    "AUTH_HEADER_PREFIX": "API-Token",
}

# Auth redirect
AUTH_USER_MODEL = "dmv_home.User"
LOGIN_REDIRECT_URL = "/app/"
LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = LOGIN_URL

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.Argon2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
#     "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
# ]

logger.info("LOG: auth module is loaded.")
