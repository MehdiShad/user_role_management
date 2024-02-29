from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import BaseUser
from user_role_management.core.exceptions import error_response, success_response


def get_users(request, **kwargs) -> QuerySet[BaseUser]:
    return BaseUser._get_all()


def get_user(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = BaseUser._get_by_id(id=id)
    if not isinstance(obj, BaseUser):
        return error_response(message="There are no record")
    return success_response(data=obj)
