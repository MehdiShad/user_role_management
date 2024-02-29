from django.http import HttpRequest
from typing import Dict, Literal
from user_role_management.manage.models import Department, Position, Employee


def create_department(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Department._create(**kwargs)


def update_department(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Department._update(id=id, **kwargs)


def create_employee(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Employee._create(**kwargs)


def update_employee(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Employee._update(id=id, **kwargs)


def create_position(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Position._create(**kwargs)


def update_position(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Position._update(id=id, **kwargs)
