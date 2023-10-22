from django.db import models
from django_fsm import FSMField, transition
from .utils import TeamRole, InvitationStatusEnum
from .user import User
from .team import Team
from rest_framework import exceptions


class Invitation(models.Model):
    """Invitation model."""

    invitor = models.ForeignKey(
        User,
        related_name="invitations",
        on_delete=models.CASCADE,
        verbose_name="Invitor",
    )
    traget_team = models.ForeignKey(
        Team,
        related_name="invitations",
        on_delete=models.CASCADE,
        verbose_name="Target Team",
    )
    target_role = models.CharField(
        max_length=7,
        choices=TeamRole.choices_tuple_list(),
        default=TeamRole.level_1.value,
    )
    all_teams = models.BooleanField(default=False, verbose_name="Invite All Teams")
    invitee_email = models.EmailField(verbose_name="Email Address", unique=False)
    status = FSMField(
        default=InvitationStatusEnum.drafted,
        choices=InvitationStatusEnum.choices_tuple_list(),
        protected=True,
        verbose_name="Invitation Status",
    )
    created = models.DateField(auto_now_add=True, verbose_name="Create")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Updated")

    @transition(
        field=status,
        source=InvitationStatusEnum.drafted,
        target="Submitted",
        permission=lambda instance, user: instance.invitor == user,
        conditions=None,
    )
    def make_submitted(self):
        pass

    @transition(
        field=status,
        source=[InvitationStatusEnum.drafted, InvitationStatusEnum.submitted],
        target=InvitationStatusEnum.cancelled,
        permission=lambda instance, user: instance.invitor == user,
    )
    def make_cancelled(self):
        pass

    @transition(
        field=status,
        source=InvitationStatusEnum.submitted,
        target=InvitationStatusEnum.rejected,
        permission=lambda instance, user: instance.invitee_email == user.email,
    )
    def make_rejected(self):
        pass

    @transition(
        field=status,
        source=[InvitationStatusEnum.submitted, InvitationStatusEnum.rejected],
        target=InvitationStatusEnum.accepted,
        permission=lambda instance, user: instance.invitor == user
        or instance.invitee_email == user.email,
    )
    def make_accepted(self):
        pass
