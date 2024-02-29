from django.http import HttpRequest
from typing import Dict, Literal
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission


def create_user_object_permission(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return UserObjectPermission._create(**kwargs)


def update_user_object_permission(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return UserObjectPermission._update(id=id, **kwargs)


def create_group_object_permission(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return GroupObjectPermission._create(**kwargs)


def update_group_object_permission(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return GroupObjectPermission._update(id=id, **kwargs)
