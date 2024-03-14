from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.manage.models import Company_position, Employee, Company_department, \
    Company_department_employee, Company_department_position


def get_positions(request: HttpRequest, **kwargs) -> QuerySet[Company_position]:
    return Company_position._get_all()


def get_position(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_position._get_by_id(id=id)
    if not isinstance(obj, Company_position):
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


def get_company_department_positions(request: HttpRequest, **kwargs) -> QuerySet[Company_department_position]:
    return Company_department_position._get_all()


def get_company_department_position(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Company_department_position._get_by_id(id=id)
    if not isinstance(obj, Company_department_position):
        return error_response(message="There are no record")
    return success_response(data=obj)
