from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib.auth.models import Permission
from user_role_management.manage.models import Company, Company_group
from user_role_management.core.exceptions import error_response, success_response


def get_permissions(request, **kwargs) -> QuerySet[Permission]:
    return Permission.objects.all()


def get_permission(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    try:
        group = Permission.objects.get(id=id)
        return success_response(data=group)
    except Exception as ex:
        return error_response(message="There are no record")
