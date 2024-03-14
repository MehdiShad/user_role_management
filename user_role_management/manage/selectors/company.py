from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib.auth.models import Group
from user_role_management.manage.models import Company, Company_group, Company_branch
from user_role_management.core.exceptions import error_response, success_response


def get_companies(request, **kwargs) -> QuerySet[Company]:
    return Company._get_all()


def get_company(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company._get_by_id(id=id)
    if not isinstance(obj, Company):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_groups(request, **kwargs) -> QuerySet[Group]:
    return Group.objects.all()


def get_group(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    try:
        group = Group.objects.get(id=id)
        return success_response(data=group)
    except Exception as ex:
        return error_response(message="There are no record")



def get_company_groups(request, **kwargs) -> QuerySet[Company_group]:
    return Company_group._get_all()


def get_company_group(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_group._get_by_id(id=id)
    if not isinstance(obj, Company_group):
        return error_response(message="There are no record")
    return success_response(data=obj)



def get_company_branches(request, **kwargs) -> QuerySet[Company_branch]:
    return Company_branch._get_all()


def get_company_branch(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_branch._get_by_id(id=id)
    if not isinstance(obj, Company_branch):
        return error_response(message="There are no record")
    return success_response(data=obj)


