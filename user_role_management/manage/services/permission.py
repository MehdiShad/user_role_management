from typing import Dict, Literal
from django.http import HttpRequest
from django.contrib.auth.models import Permission
from user_role_management.utils.services import create_fields
from user_role_management.core.exceptions import error_response, success_response


def create_permission(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    try:
        fields = create_fields(**kwargs)
        new = Permission.objects.create(**fields)
        return success_response(data=new)
    except Exception as ex:
        return error_response(message=str(ex))


def update_permission(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    try:
        obj = Permission.objects.get(id=id)
        fields = create_fields(**kwargs)
        obj.__dict__.update(**fields)
        obj.save()
        return success_response(data=obj)
    except Exception as ex:
        return error_response(message=str(ex))
