import structlog
from django.views.generic import RedirectView

logger = structlog.get_logger(__name__)

class CustomRedirectView(RedirectView):
    permanent = False
    url = "/"

    def get_redirect_url(self, *args, **kwargs):
        return self.url
