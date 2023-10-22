from django.contrib.auth.backends import BaseBackend
from .models import User


class EmailAuthenticationBackend(BaseBackend):
    def authenticate(self, **kwargs):
        email = kwargs[
            "username"
        ].lower()  # If you made email case insensitive add lower()
        password = kwargs["password"]
        try:
            my_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if my_user.is_active and my_user.check_password(password):
                return my_user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
