from typing import Optional
from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.manage.models import Process, Action
from user_role_management.guardian.shortcuts import get_objects_for_user
from django.contrib.auth.decorators import login_required, permission_required


def get_processes(request: HttpRequest) -> QuerySet[Process]:
    # process = get_objects_for_user(request.user, "manage.view_process", klass=Process)
    process = get_objects_for_user(request.user, "manage.dg_can_view_process", klass=Process)
    return process

def get_process(request: HttpRequest, id: int) -> Optional[Action]:
    return Process._get_by_id(id=id)


def get_actions(request, **kwargs) -> QuerySet[Action]:
    return Action._get_all()


def get_action(request: HttpRequest, id: int) -> Optional[Action]:
    return Action._get_by_id(id=id)
