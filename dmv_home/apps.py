from django.apps import AppConfig


class DmvHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dmv_home'

    def ready(self) -> None:
        from . import signals
        return super().ready()