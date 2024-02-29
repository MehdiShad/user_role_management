from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Department, Position, Employee
from user_role_management.core.exceptions import error_response, success_response

def get_departments(request: HttpRequest, **kwargs) -> QuerySet[Department]:
    return Department._get_all()


def get_department(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Department._get_by_id(id=id)
    if not isinstance(obj, Department):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_positions(request: HttpRequest, **kwargs) -> QuerySet[Department]:
    return Position._get_all()


def get_position(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Position._get_by_id(id=id)
    if not isinstance(obj, Position):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_employees(request: HttpRequest, **kwargs) -> QuerySet[Employee]:
    return Employee._get_all()


def get_employee(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Employee._get_by_id(id=id)
    if not isinstance(obj, Employee):
        return error_response(message="There are no record")
    return success_response(data=obj)
