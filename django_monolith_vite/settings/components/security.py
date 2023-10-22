from typing import Dict, List, Union

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # * « True - CSRF not found error could be shown up.
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "SAMEORIGIN"

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "strict-origin-when-cross-origin"

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234
