from django.http import HttpRequest
from typing import Dict, Literal
from user_role_management.manage.models import Company


def create_company(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company._create(**kwargs)


def update_company(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company._update(id=id, **kwargs)