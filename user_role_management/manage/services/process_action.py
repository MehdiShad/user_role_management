from typing import Dict, Literal
from django.http import HttpRequest
from user_role_management.manage.models import BaseUser, Process, Action
from django.contrib.auth.decorators import login_required, permission_required
from user_role_management.core.exceptions import error_response, success_response


# @login_required
# @permission_required(
#     {
#         ("manage.add_process"),
#         ("manage.dg_can_start_process"),
#     }, raise_exception=True
# )
def create_process(reqeust: HttpRequest, **kwargs):
    try:
        user = reqeust.user
        if 'company_id' in kwargs:
            company_id = kwargs['company_id']
        else:
            company_id = user.last_company_logged_in_id
        process = Process.objects.create(name=kwargs.get("name"), created_by=user, company_id=company_id)
        return success_response(data=process)
    except Exception as ex:
        return error_response(message=str(ex))


def update_process(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Process._update(id=id, **kwargs)


def create_action(*, request: HttpRequest, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Action._create(**kwargs)


def update_action(*, request: HttpRequest, id: int, **kwargs) -> Dict[str, Literal['is_success', True, False]]:
    return Action._update(id=id, **kwargs)
