from typing import Optional
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Department, Position, Employee


def get_departments(request: HttpRequest, **kwargs) -> QuerySet[Department]:
    return Department._get_all()


def get_department(request: HttpRequest, id: int) -> Optional[Department]:
    return Department._get_by_id(id=id)


def get_positions(request: HttpRequest, **kwargs) -> QuerySet[Department]:
    return Position._get_all()


def get_position(request: HttpRequest, id: int) -> Optional[Department]:
    return Position._get_by_id(id=id)


def get_employees(request: HttpRequest, **kwargs) -> QuerySet[Employee]:
    return Employee._get_all()


def get_employee(request: HttpRequest, id: int) -> Optional[Employee]:
    return Employee._get_by_id(id=id)
