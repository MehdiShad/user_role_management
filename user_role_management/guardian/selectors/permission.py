from typing import Optional
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission


def get_user_object_permissions(request, **kwargs) -> QuerySet[UserObjectPermission]:
    return UserObjectPermission._get_all()


def get_user_object_permission(request: HttpRequest, id: int) -> Optional[UserObjectPermission]:
    return UserObjectPermission._get_by_id(id=id)


def get_group_object_permissions(request, **kwargs) -> QuerySet[GroupObjectPermission]:
    return GroupObjectPermission._get_all()


def get_group_object_permission(request: HttpRequest, id: int) -> Optional[GroupObjectPermission]:
    return GroupObjectPermission._get_by_id(id=id)
