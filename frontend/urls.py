from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^public/.*$", views.public_index, name="app_public"),
    re_path(r"^$", views.index, name="app_private"),
    re_path(r"^(?:.*)/?$", views.index),
]
