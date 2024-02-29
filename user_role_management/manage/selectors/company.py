from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Company
from user_role_management.core.exceptions import error_response, success_response

def get_companies(request, **kwargs) -> QuerySet[Company]:
    return Company._get_all()


def get_company(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company._get_by_id(id=id)
    if not isinstance(obj, Company):
        return error_response(message="There are no record")
    return success_response(data=obj)