import os

# Email configuration
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_HOST_USER = "minminlaxz@gmail.com"
DEFAULT_FROM_EMAIL = "minlaxz.io <minminlaxz@gmail.com>"
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
SENDGRID_SANDBOX_MODE_IN_DEBUG = True
SENDGRID_ECHO_TO_STDOUT = True
#