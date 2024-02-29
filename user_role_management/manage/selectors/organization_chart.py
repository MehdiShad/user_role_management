from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.manage.models import Department, Position, Employee, Company_department, \
    Company_department_employee


def get_departments(request: HttpRequest, **kwargs) -> QuerySet[Department]:
    return Department._get_all()


def get_department(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Department._get_by_id(id=id)
    if not isinstance(obj, Department):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_positions(request: HttpRequest, **kwargs) -> QuerySet[Position]:
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


def get_company_departments(request: HttpRequest, **kwargs) -> QuerySet[Company_department]:
    return Company_department._get_all()


def get_company_department(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_department._get_by_id(id=id)
    if not isinstance(obj, Company_department):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_company_department_employees(request: HttpRequest, **kwargs) -> QuerySet[Company_department_employee]:
    return Company_department_employee._get_all()


def get_company_department_employee(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_department_employee._get_by_id(id=id)
    if not isinstance(obj, Company_department_employee):
        return error_response(message="There are no record")
    return success_response(data=obj)
