from django.http import HttpRequest
from typing import Dict, Literal
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.guardian.models.models import GroupObjectPermission, UserObjectPermission
from user_role_management.manage.models import Department, Position, Employee, Company_department, Company_department_employee, Action, Process


def create_department(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Department._create(**kwargs)


def update_department(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Department._update(id=id, **kwargs)


def create_employee(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    # check access to register new employee
    user = request.user
    last_company_id = user.last_company_logged_in
    company_groups = user.company_groups.all()
    process = Process.objects.filter(name='user_management').last()
    if not process:
        return error_response(message='There is no process')
    process_id = process.id
    has_action_access = Action.objects.filter(process_id=process_id, title='can_add_employee').last()
    if not has_action_access:
        return error_response(message='There is no action')
    all_action_permissions = GroupObjectPermission.objects.filter(group_id__in=company_groups, permission__codename='dg_can_do_this_action', content_type__model='action')
    if not all_action_permissions:
        return error_response(message="You are not authorized to add new employees")
    action_ids = list(all_action_permissions.values_list('object_pk', flat=True))
    has_permission = Action.objects.filter(pk__in=action_ids, title='can_add_employee').last()
    if not has_permission:
        return error_response(message="You are not authorized to add new employees")

    return Employee._create(**kwargs)


def update_employee(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Employee._update(id=id, **kwargs)


def create_position(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Position._create(**kwargs)


def update_position(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Position._update(id=id, **kwargs)


def create_company_department(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department._create(**kwargs)


def update_company_department(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department._update(id=id, **kwargs)




def create_company_department_employee(request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_employee._create(**kwargs)


def update_company_department_employee(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Company_department_employee._update(id=id, **kwargs)