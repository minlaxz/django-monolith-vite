import structlog

from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from dmv_home.models import User


logger = structlog.get_logger(__name__)


@receiver(user_signed_up, sender=User)
def user_signed_up_callback(sender, user, **kwargs):
    logger.info(f"User is signed up: {user.email}")


@receiver(pre_social_login, sender=User)
def pre_social_login_callback(sender, sociallogin, **kwargs):
    logger.info(f"Social User is logging in -- pre: {sociallogin.user.email}")


@receiver(user_logged_out, sender=User)
def user_logged_out_callback(sender, user, **kwargs):
    logger.info(f"User is logging out: {user.email}")


# * user logging in using allauth backend (using sso)
@receiver(user_logged_in, sender=User)
def user_logged_in_callback(sender, user, **kwargs):
    logger.info(f"User is logging in: {user.email}")
