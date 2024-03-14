from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib.auth.models import Permission
from user_role_management.manage.models import BaseUser
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.manage.filters import user as user_filter


def get_users(request, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}
    user = request.user
    qs = BaseUser.filtered_by_company(company=user.last_company_logged_in).order_by('-id')
    return user_filter.UsersFilter(filters, qs).qs


def get_user(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = BaseUser._get_by_id(id=id)
    if not isinstance(obj, BaseUser):
        return error_response(message="There are no record")
    return success_response(data=obj)
