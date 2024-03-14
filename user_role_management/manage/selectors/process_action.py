from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Process, Action
from user_role_management.guardian.shortcuts import get_objects_for_user
from django.contrib.auth.decorators import login_required, permission_required
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.manage.filters import process_action as process_action_filters


def get_processes(request: HttpRequest) -> QuerySet[Process]:
    # process = get_objects_for_user(request.user, "manage.view_process", klass=Process)
    process = get_objects_for_user(request.user, "manage.dg_can_view_process", klass=Process)
    return process


def get_filtered_processes(request: HttpRequest, filters=None) -> QuerySet[Process]:
    filters = filters or {}
    user = request.user
    qs = Process.filtered_by_company(company=user.last_company_logged_in).order_by('-id')
    return process_action_filters.ProcessFilter(filters, qs).qs


def get_process(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Process._get_by_id(id=id)
    if not isinstance(obj, Process):
        return error_response(message="There are no record")
    return success_response(data=obj)


def get_actions(request, **kwargs) -> QuerySet[Action]:
    return Action._get_all()


def get_filtered_actions(request: HttpRequest, filters=None) -> QuerySet[Action]:
    filters = filters or {}
    user = request.user
    qs = Action.filtered_by_company(company=user.last_company_logged_in).order_by('-id')
    return process_action_filters.ActionFilter(filters, qs).qs


def get_action(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    obj = Action._get_by_id(id=id)
    if not isinstance(obj, Action):
        return error_response(message="There are no record")
    return success_response(data=obj)
