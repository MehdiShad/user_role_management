from typing import Optional
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Company


def get_companies(request, **kwargs) -> QuerySet[Company]:
    return Company._get_all()


def get_company(request: HttpRequest, id: int) -> Optional[Company]:
    return Company._get_by_id(id=id)