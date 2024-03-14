from django.http import HttpRequest
from typing import Dict, Literal
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.guardian.models.models import GroupObjectPermission, UserObjectPermission
from user_role_management.manage.models import Company_position, Employee, Company_department, Company_department_employee, Action, Process, Company_department_position
from user_role_management.core.permission import url_action_perm



def create_employee(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Employee._create(**kwargs)


def update_employee(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Employee._update(id=id, **kwargs)


def create_position(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_position._create(**kwargs)


def update_position(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_position._update(id=id, **kwargs)


def create_company_department(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department._create(**kwargs)


def update_company_department(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department._update(id=id, **kwargs)




def create_company_department_employee(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_employee._create(**kwargs)


def update_company_department_employee(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_employee._update(id=id, **kwargs)




def create_company_department_position(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_position._create(**kwargs)


def update_company_department_position(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_position._update(id=id, **kwargs)