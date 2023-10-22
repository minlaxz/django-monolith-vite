import structlog
from allauth.socialaccount.adapter import get_adapter
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from dmv_home.models import User, Invitation
from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm


logger = structlog.getLogger(__name__)


class UserSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    organization_name = forms.CharField(widget=forms.TextInput())

    field_order = ["email", "password1", "password2", "organization_name", "captcha"]

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        return user

    def signup(self, request, user):
        pass


class UserLoginForm(AuthenticationForm):
    # username is acutally email field but to comply with AuthenticationForm
    # it has to be named as username.
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "validate", "id": "field_email"})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"class": "validate", "id": "field_password"}),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)


class UserPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    # Override saving function
    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        html_email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        **kwargs,
    ):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        try:
            # this is the same = self.cleaned_data['email'] == request.POST['email']
            user = User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            logger.warn(
                f'user {request.POST["email"]} requested for reset but does not exist.'
            )
            return
        link = request.build_absolute_uri(
            reverse(
                "password_reset_confirm",
                kwargs={
                    "uidb64": urlsafe_base64_encode(force_bytes((user.pk))),
                    "token": token_generator.make_token(user),
                },
            )
        )
        # {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
        # utils.send_reset_link(email=user.email, link=link)


social_signup_read_only_fields = ["email"]


class CustomSocialSignupForm(SocialSignupForm):
    organization_name = forms.CharField(widget=forms.TextInput())
    
    field_order = ["email", "organization_name"]

    def __init__(self, *args, **kwargs):
        super(CustomSocialSignupForm, self).__init__(*args, **kwargs)

        self.first_invited_object = Invitation.objects.filter(
            invitee_email=kwargs.get("sociallogin").user.email
        ).first()
        self.invitation_exists = True if self.first_invited_object else False
        self.organization_name = (
            self.first_invited_object.sent_by.organization
            if self.invitation_exists
            else None
        )

        self.fields["organization_name"].required = (
            False if self.first_invited_object else True
        )

        for f in social_signup_read_only_fields:
            self.fields[f].disabled = True

    def save(self, request):
        adapter = get_adapter()
        user = adapter.save_user(request, self.sociallogin, form=self)
        self.custom_signup(request, user)
        return user

    # def save(self, request):

    #     # Ensure you call the parent class's save.
    #     # .save() returns a User object.
    #     user = super(SocialSignupForm, self).save(request)

    #     # Add your own processing here.

    #     # You must return the original result.
    #     return user