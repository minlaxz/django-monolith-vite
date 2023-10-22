import logging
import json
import base64
import six

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from django_fsm import FSMField, has_transition_perm
from django.db import transaction, models
from django.core.exceptions import FieldDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.crypto import get_random_string
from allauth.utils import SERIALIZED_DB_FIELD_PREFIX


from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

# from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .models import User, Invitation, Organization, Team

logger = logging.getLogger(__name__)


def custom_serializer(instance):
    data = {}
    for k, v in instance.__dict__.items():
        if k.startswith("_") or callable(v):
            continue
        try:
            field = instance._meta.get_field(k)
            if isinstance(field, models.BinaryField):
                v = force_text(base64.b64encode(v))
            elif isinstance(field, models.FileField):
                if v and not isinstance(v, six.string_types):
                    v = {
                        "name": v.name,
                        "content": base64.b64encode(v.read()).decode("ascii"),
                    }
            elif isinstance(field, FSMField):
                v = six.text_type(v.value)
            # Check if the field is serializable. If not, we'll fall back
            # to serializing the DB values which should cover most use cases.
            try:
                json.dumps(v, cls=DjangoJSONEncoder)
            except TypeError:
                v = field.get_prep_value(v)
                k = SERIALIZED_DB_FIELD_PREFIX + k
        except FieldDoesNotExist:
            pass

        # remove status, it's potected in FSMField
        if k not in ["status", "sociallogin"]:
            data[k] = v

    return json.loads(json.dumps(data, cls=DjangoJSONEncoder))


class CustomAccountAdapter(DefaultAccountAdapter):
    def __init__(self, request=None):
        super().__init__(request)

    def setup_user(self, request, user: User, form):
        with transaction.atomic():
            organization = Organization.objects.create(
                name=f"{user.email}-{form.cleaned_data.get('organization_name', 'N/A')}",
                prefix=get_random_string(length=16),
                quantity=10,
            )
            user.organization = organization
            user.save()
            # FSM and Guardian setup
            organization.make_org_6(user=user)
            if has_transition_perm(organization.make_active, user=user):
                organization.make_active()
                organization.save()

            team = Team.objects.create(
                name="Default Team",
            )
            team.members.add(user)
            team.organization = organization
            team.save()
            # FSM and Guardian setup
            team.make_level_4(user=user)
            if has_transition_perm(team.make_active, user=user):
                team.make_active()
                team.save()

            if has_transition_perm(user.make_active, user=user):
                user.make_active()
                user.save()

    def new_user(self, request):
        return super().new_user(request)

    def populate_username(self, request, user):
        return super().populate_username(request, user)

    def save_user(self, request, user, form, commit=True):
        # user = setup_user(user, False, form)
        # user = setup_info(user, inv)
        self.setup_user(request, user, form)

        # This will be called regardless of SSO or normal signup
        return super().save_user(request, user, form, commit)

    def login(self, request, user):
        logger.info(">>> Logged the user in ...")
        return super().login(request, user)

    def is_open_for_signup(self, request):
        return True  # Signup will also be handled by the API


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def __init__(self, request=None):
        super().__init__()

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        existing_social_account = SocialAccount.objects.filter(
            user__email=user.email
        ).first()
        if sociallogin.is_existing:
            # * Existing social account, login the user
            return
        if not sociallogin.is_existing:
            # ! Existing social account with different provider, not allowed
            if existing_social_account:
                request.session["ef_not_allowed"] = 1
                raise ImmediateHttpResponse(
                    HttpResponseRedirect(reverse("socialaccount_login_error"))
                )
        if not sociallogin.email_addresses:
            # ! New user but no email address, maybe using phone number, and we need email address
            return
        verified_email = None
        for email in sociallogin.email_addresses:
            if email.verified:
                # * Take the first verified email address
                verified_email = email
                break
        if not verified_email:
            # ! New user with email address, but not verified by the SSO provider, maybe abusing other user's account
            return

        try:
            # *** Check if the manually signed up user, and connect if exists
            u = User.objects.get(
                email=user.email, is_active=True
            )  # status="unactivated")
            sociallogin.connect(request, u)
        except User.DoesNotExist:
            # *** This is a new user, sign up from SSO provider
            pass

        # ** Hang over to save_user **
        return super().pre_social_login(request, sociallogin)

    def serialize_instance(self, instance):
        # return super().serialize_instance(instance)
        # * User.status is FSMField which need to be serialized by hand
        # * Otherwise, serialization will fail.
        return custom_serializer(instance=instance)

    def deserialize_instance(self, model, data):
        return super().deserialize_instance(model, data)

    def save_user(self, request, sociallogin, form=None):
        return super().save_user(request, sociallogin, form)

    def is_open_for_signup(self, request, socialaccount):
        return True
