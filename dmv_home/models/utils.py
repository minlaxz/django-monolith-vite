from uuid import uuid4
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from enum import Enum


def path_and_rename(instance, filename):
    upload_to = "images"
    ext = filename.split(".")[-1]
    # set filename as random string
    filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = settings.MAX_PROFILE_IMAGE_SIZE
    if filesize > megabyte_limit:
        raise ValidationError(
            "Max file size is %sMB" % str(megabyte_limit / 1024 / 1024)
        )


class UserStatusEnum(Enum):
    unactivated = "unactivated"
    activated = "activated"
    deactivated = "deactivated"

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices_list(cls):
        return [(role.value.lower()) for role in cls]

    @classmethod
    def choices_tuple_list(cls):
        return [(role.value.lower(), role.value.lower()) for role in cls]


class TeamStatusEnum(Enum):
    unactivated = "unactivated"
    activated = "activated"
    deactivated = "deactivated"

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices_list(cls):
        return [(role.value.lower()) for role in cls]

    @classmethod
    def choices_tuple_list(cls):
        return [(role.value.lower(), role.value.lower()) for role in cls]


class OrganizationStatusEnum(Enum):
    unactivated = "unactivated"
    activated = "activated"
    deactivated = "deactivated"

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices_list(cls):
        return [(role.value.lower()) for role in cls]

    @classmethod
    def choices_tuple_list(cls):
        return [(role.value.lower(), role.value.lower()) for role in cls]


class InvitationStatusEnum(Enum):
    drafted = "drafted"
    submitted = "submitted"
    cancelled = "cancelled"
    rejected = "rejected"
    accepted = "accepted"

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices_list(cls):
        return [(role.value.lower()) for role in cls]

    @classmethod
    def choices_tuple_list(cls):
        return [(role.value.lower(), role.value.lower()) for role in cls]


class TeamRole(Enum):
    level_1 = "level_1"  # lowest permission
    level_2 = "level_2"
    level_3 = "level_3"
    level_4 = "level_4"  # highest permission

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices_list(cls):
        return [(role.value.lower()) for role in cls]

    @classmethod
    def choices_tuple_list(cls):
        return [(role.value.lower(), role.value.lower()) for role in cls]


class OrganizationRole(Enum):
    org_6 = "org_6"
    org_4 = "org_4"

    @property
    def verbose_name(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(role.value.lower()) for role in cls]


def team_attachment(instance, filename):
    upload_to = "attachements/teams/"
    if instance.qsmain.team:
        tmid = instance.qsmain.team.tmid
    else:
        tmid = instance.qsmain.project.team.tmid
    ext = filename.split(".")[-1]
    # set filename as random string
    filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, str(tmid), str(filename))
