# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import Group, GroupManager

from guardian.shortcuts import assign_perm, get_perms, get_users_with_perms, remove_perm
from django_fsm import FSMField, transition

from .user import User
from .utils import (
    TeamRole,
    TeamStatusEnum,
    team_attachment,
    path_and_rename,
    validate_image,
)


class Team(models.Model):
    """Team model."""

    name = models.CharField(max_length=255, verbose_name="Name")
    created = models.DateField(auto_now_add=True, verbose_name="Created Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    logo = models.ImageField(
        upload_to=path_and_rename,
        validators=[validate_image],
        blank=True,
        null=True,
        verbose_name="Team Logo",
    )
    members = models.ManyToManyField(
        "dmv_home.User", blank=True, related_name="teams", verbose_name="Members"
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="teams",
        verbose_name="Organization",
    )
    status = FSMField(
        default=TeamStatusEnum.unactivated,
        choices=TeamStatusEnum.choices_tuple_list(),
        protected=True,
        verbose_name="Team Status",
    )

    class Meta:
        ordering = ("-pk",)
        permissions = (
            (TeamRole.level_1.value, "View Permission"),
            (TeamRole.level_2.value, "Edit Permission"),
            (TeamRole.level_3.value, "Change Permission"),
            (TeamRole.level_4.value, "Full Permission"),
        )

    def __str__(self):
        return f"{self.name}-T{self.pk}"

    def grant_perm(self, user: User, role: TeamRole):
        assign_perm(role.value, user, self)

    def purge_perm(self, user: User, role: TeamRole):
        remove_perm(role.value, user, self)

    def add_level_1(self, user: User):
        self.members.add(user)
        self.grant_perm(user, TeamRole.level_1)

    def add_level_2(self, user: User):
        self.members.add(user)
        self.grant_perm(user, TeamRole.level_1)
        self.grant_perm(user, TeamRole.level_2)

    def add_level_3(self, user: User):
        self.members.add(user)
        self.grant_perm(user, TeamRole.level_1)
        self.grant_perm(user, TeamRole.level_2)
        self.grant_perm(user, TeamRole.level_3)

    def add_level_4(self, user: User):
        self.members.add(user)
        self.grant_perm(user, TeamRole.level_1)
        self.grant_perm(user, TeamRole.level_2)
        self.grant_perm(user, TeamRole.level_3)
        self.grant_perm(user, TeamRole.level_4)

    def make_level_4(self, user: User):
        _perms = get_perms(user, self)
        if TeamRole.level_1.value not in _perms:
            self.grant_perm(user, TeamRole.level_1)
        if TeamRole.level_2.value not in _perms:
            self.grant_perm(user, TeamRole.level_2)
        if TeamRole.level_3.value not in _perms:
            self.grant_perm(user, TeamRole.level_3)
        if TeamRole.level_4.value not in _perms:
            self.grant_perm(user, TeamRole.level_4)

    def make_level_3(self, user: User):
        _perms = get_perms(user, self)
        if TeamRole.level_4.value in _perms:
            self.purge_perm(user, TeamRole.level_4)
        if TeamRole.level_3.value not in _perms:
            self.grant_perm(user, TeamRole.level_3)
        if TeamRole.level_2.value not in _perms:
            self.grant_perm(user, TeamRole.level_2)
        if TeamRole.level_1.value not in _perms:
            self.grant_perm(user, TeamRole.level_1)

    def make_level_2(self, user: User):
        _perms = get_perms(user, self)
        if TeamRole.level_4.value in _perms:
            self.purge_perm(user, TeamRole.level_4)
        if TeamRole.level_3.value in _perms:
            self.purge_perm(user, TeamRole.level_3)
        if TeamRole.level_2.value not in _perms:
            self.grant_perm(user, TeamRole.level_2)
        if TeamRole.level_1.value not in _perms:
            self.grant_perm(user, TeamRole.level_1)

    def make_level_1(self, user: User):
        _perms = get_perms(user, self)
        if TeamRole.level_4.value in _perms:
            self.purge_perm(user, TeamRole.owner)
        if TeamRole.level_3.value in _perms:
            self.purge_perm(user, TeamRole.approver)
        if TeamRole.level_2.value in _perms:
            self.purge_perm(user, TeamRole.estimator)
        if TeamRole.level_1.value not in _perms:
            self.grant_perm(user, TeamRole.watcher)

    def remove_member(self, user: User):
        self.purge_perm(user, TeamRole.level_1)
        self.purge_perm(user, TeamRole.level_2)
        self.purge_perm(user, TeamRole.level_3)
        self.purge_perm(user, TeamRole.level_4)
        self.members.remove(user)

    def get_level_4s(self) -> list:
        return get_users_with_perms(
            self, only_with_perms_in=[TeamRole.level_4.value], with_superusers=False
        )

    def get_level_3s(self) -> list:
        return get_users_with_perms(
            self, only_with_perms_in=[TeamRole.level_3.value], with_superusers=False
        )

    def get_level_2s(self) -> list:
        return get_users_with_perms(
            self, only_with_perms_in=[TeamRole.level_2.value], with_superusers=False
        )

    def get_level_1s(self) -> list:
        return get_users_with_perms(
            self, only_with_perms_in=[TeamRole.level_1.value], with_superusers=False
        )

    def is_level_4(self, user: User) -> bool:
        return user in self.get_level_4s()

    def is_level_3(self, user: User) -> bool:
        return user in self.get_level_3s()

    def is_level_2(self, user: User) -> bool:
        return user in self.get_level_2s()

    def is_level_1(self, user: User) -> bool:
        return user in self.get_level_1s()

    @transition(
        field=status,
        source=TeamStatusEnum.unactivated,
        target=TeamStatusEnum.activated,
        permission=lambda instance, user: instance.is_level_4(user),
    )
    def make_active(self):
        pass

    @transition(
        field=status,
        source=TeamStatusEnum.activated,
        target=TeamStatusEnum.unactivated,
        permission=lambda instance, user: instance.is_level_4(user),
    )
    def make_inactive(self):
        pass

    @transition(
        field=status,
        source=TeamStatusEnum.unactivated,
        target=TeamStatusEnum.deactivated,
        permission=lambda instance, user: instance.is_level_4(user),
    )
    def make_deactive(self):
        pass
