from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from user_role_management.manage.models import Process, Action
from user_role_management.core.messages import errors as err_message
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission


def url_action_perm(*, process_name: str, action_name: str, permission_codename: str):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            user = request.user
            last_company_id = user.last_company_logged_in
            if not last_company_id:
                return Response(error_response(message=err_message.EMPTY_COMPANY), status=status.HTTP_404_NOT_FOUND)
            company_groups = user.company_groups.all()
            process = Process.objects.filter(name=process_name, company_id=last_company_id).last()
            if not process:
                return Response(error_response(message=err_message.NOT_FOUND_PROCESS_MESSAGE.format(process_name=process_name)), status=status.HTTP_404_NOT_FOUND)

            all_action_permissions = GroupObjectPermission.objects.filter(group_id__in=company_groups, permission__codename=permission_codename, content_type__model='action')
            if not all_action_permissions:
                return Response(error_response(message=err_message.UNAUTHORIZED_ACTION), status=status.HTTP_401_UNAUTHORIZED)

            action_ids = list(all_action_permissions.values_list('object_pk', flat=True))
            has_permission = Action.objects.filter(pk__in=action_ids, code_name=action_name, process_id=process.id).last()
            if not has_permission:
                return Response(error_response(message=err_message.UNAUTHORIZED_ACTION), status=status.HTTP_401_UNAUTHORIZED)
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator

