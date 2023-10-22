from typing import TYPE_CHECKING, Callable

import structlog

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class LoggingContextVarsMiddleware(object):
    """Used to reset ContextVars in structlog on each request."""

    def __init__(
        self,
        get_response: "Callable[[HttpRequest], HttpResponse]",
    ) -> None:
        """Django's API-compatible constructor."""
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        """
        Handle requests.
        Add your logging metadata here.
        Example: https://github.com/jrobichaud/django-structlog
        """
        response = self.get_response(request)
        structlog.contextvars.clear_contextvars()
        return response
