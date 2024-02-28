from django.http import HttpRequest
from django.db.models import QuerySet
from user_role_management.users.models import Process
from user_role_management.guardian.shortcuts import get_objects_for_user
from django.contrib.auth.decorators import login_required, permission_required


def get_all_processes(request: HttpRequest) -> QuerySet[Process]:
    # process = get_objects_for_user(request.user, "users.view_process", klass=Process)
    process = get_objects_for_user(request.user, "users.dg_can_view_process", klass=Process)
    return process