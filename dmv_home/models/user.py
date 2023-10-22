from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_fsm import FSMField, transition
from .utils import UserStatusEnum, path_and_rename, validate_image


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("You must register with a valid email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must be registered with is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must be registered with is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    country = models.CharField(max_length=255, verbose_name="Country")
    language = models.CharField(max_length=255, verbose_name="Language")
    about = models.TextField(blank=True, null=True, verbose_name="About Me")
    is_active = models.BooleanField(verbose_name="Custom Active", default=False)
    is_superuser = models.BooleanField(verbose_name="Custom Superuser", default=False)
    created = models.DateField(auto_now_add=True, verbose_name="Created Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    status = FSMField(
        default=UserStatusEnum.unactivated,
        choices=UserStatusEnum.choices_tuple_list(),
        protected=True,
        verbose_name="User Status",
    )

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Organization",
    )
    image = models.ImageField(
        upload_to=path_and_rename,
        validators=[validate_image],
        blank=True,
        null=True,
        verbose_name="Profile Image",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "country", "language", "status"]
    objects = UserManager()

    @transition(
        field=status,
        source=UserStatusEnum.unactivated,
        target=UserStatusEnum.activated,
        permission=lambda instance, user: instance == user,
    )
    def make_active(self):
        self.is_active = True

    @transition(
        field=status,
        source=UserStatusEnum.activated,
        target=UserStatusEnum.unactivated,
        permission=lambda instance, user: instance == user,
    )
    def make_inactive(self):
        pass

    @transition(
        field=status,
        source=UserStatusEnum.unactivated,
        target=UserStatusEnum.deactivated,
        permission=lambda instance, user: instance == user,
    )
    def make_deactive(self):
        pass
