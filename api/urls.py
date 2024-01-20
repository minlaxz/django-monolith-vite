from django.urls import include, path
from rest_framework import routers

urlpatterns = []

router = routers.DefaultRouter()
router.register(r"", home.UserViewSet, basename="user")
urlpatterns += [
    path("v2/", include((router.urls, "api"), namespace="api")),
]