from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission
from user_role_management.core.exceptions import error_response, success_response


def get_user_object_permissions(request, **kwargs) -> QuerySet[UserObjectPermission]:
    return UserObjectPermission._get_all()


def get_user_object_permission(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = UserObjectPermission._get_by_id(id=id)
    if not isinstance(obj, UserObjectPermission):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_group_object_permissions(request, **kwargs) -> QuerySet[GroupObjectPermission]:
    return GroupObjectPermission._get_all()


def get_group_object_permission(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = GroupObjectPermission._get_by_id(id=id)
    if not isinstance(obj, GroupObjectPermission):
        return error_response(message="There are no record")
    return success_response(data=obj)
