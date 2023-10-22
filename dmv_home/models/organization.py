from django.db import models
from django_fsm import FSMField, transition
from .utils import (
    OrganizationRole,
    OrganizationStatusEnum,
    path_and_rename,
    validate_image,
)
from guardian.shortcuts import get_perms, assign_perm, remove_perm, get_users_with_perms


class Organization(models.Model):
    """Organization model."""

    name = models.CharField(max_length=255, verbose_name="Name")
    prefix = models.CharField(max_length=16, verbose_name="Internal Prefix")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    activated = models.BooleanField(default=False, verbose_name="Activated")
    quantity = models.IntegerField(default=0, verbose_name="Quantity")
    created = models.DateField(auto_now_add=True, verbose_name="Created Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    status = FSMField(
        default=OrganizationStatusEnum.unactivated,
        choices=OrganizationStatusEnum.choices_tuple_list(),
        protected=True,
        verbose_name="Organization Status",
    )
    logo = models.ImageField(
        upload_to=path_and_rename,
        validators=[validate_image],
        blank=True,
        null=True,
        verbose_name="Organization Logo",
    )

    class Meta:
        ordering = ("-pk",)
        permissions = (
            (OrganizationRole.org_4.value, "View Permission"),
            (OrganizationRole.org_6.value, "Full Permission"),
        )

    def __str__(self):
        return self.name

    @transition(
        field=status,
        source=OrganizationStatusEnum.unactivated,
        target=OrganizationStatusEnum.activated,
        permission=lambda instance, user: instance.is_org_6(user),
    )
    def make_active(self):
        self.activated = True

    @transition(
        field=status,
        source=OrganizationStatusEnum.activated,
        target=OrganizationStatusEnum.unactivated,
        permission=lambda instance, user: instance.is_org_6(user),
    )
    def make_inactive(self):
        pass

    @transition(
        field=status,
        source=[OrganizationStatusEnum.activated, OrganizationStatusEnum.unactivated],
        target=OrganizationStatusEnum.deactivated,
        permission=lambda instance, user: instance.is_org_6(user),
    )
    def make_deactive(self):
        pass

    def make_org_6(self, user):
        _perms = get_perms(user, self)
        if OrganizationRole.org_4.value in _perms:
            remove_perm(OrganizationRole.org_4.value, user, self)
        if OrganizationRole.org_6.value not in _perms:
            assign_perm(OrganizationRole.org_6.value, user, self)

    def make_org_4(self, user):
        _perms = get_perms(user, self)
        if OrganizationRole.org_4.value not in _perms:
            assign_perm(OrganizationRole.org_4.value, user, self)
        if OrganizationRole.org_6.value in _perms:
            remove_perm(OrganizationRole.org_6.value, user, self)

    def get_org_6s(self) -> list:
        return get_users_with_perms(
            self,
            only_with_perms_in=[OrganizationRole.org_6.value],
            with_superusers=False,
        )

    def get_org_4s(self) -> list:
        return get_users_with_perms(
            self,
            only_with_perms_in=[OrganizationRole.org_4.value],
            with_superusers=False,
        )

    def is_org_6(self, user) -> bool:
        return user in self.get_org_6s()

    def is_org_4(self, user) -> bool:
        return user in self.get_org_4s()
