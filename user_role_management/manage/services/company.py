from django.http import HttpRequest
from typing import Dict, Literal
from django.contrib.auth.models import Group
from user_role_management.utils.services import create_fields
from user_role_management.manage.models import Company, Company_group
from user_role_management.core.exceptions import error_response, success_response


def create_company(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company._create(**kwargs)


def update_company(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company._update(id=id, **kwargs)


def create_group(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    try:
        fields = create_fields(**kwargs)
        new = Group.objects.create(**fields)
        return success_response(data=new)
    except Exception as ex:
        return error_response(message=str(ex))


def update_group(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    try:
        obj = Group.objects.get(id=id)
        fields = create_fields(**kwargs)
        obj.__dict__.update(**fields)
        obj.save()
        return success_response(data=obj)
    except Exception as ex:
        return error_response(message=str(ex))


def create_company_group(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_group._create(**kwargs)


def update_company_group(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_group._update(id=id, **kwargs)
