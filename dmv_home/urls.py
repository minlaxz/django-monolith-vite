from django.urls import path
from .views import CustomRedirectView


redirect_allauth_login_view = CustomRedirectView.as_view(url="/accounts/login/")


urlpatterns = [
    path("", redirect_allauth_login_view, name="signin"),
]