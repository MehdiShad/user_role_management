from functools import wraps
from rest_framework.response import Response
from user_role_management.manage.models import Process, Action
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission


def has_action_perm(*, process_name: str, action_name: str, permission_codename: str):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def decorator(view_func):
        @wraps
        def wrapper(self, request, *args, **kwargs):
            user = request.user
            last_company_id = user.last_company_logged_in
            company_groups = user.company_groups.all()
            process = Process.objects.filter(name=process_name, company_id=last_company_id).last()
            if not process:
                return error_response(message='There is no process')
            process_id = process.id
            has_action_access = Action.objects.filter(process_id=process_id, name=action_name).last()
            if not has_action_access:
                return error_response(message='There is no action')

            all_action_permissions = GroupObjectPermission.objects.filter(group_id__in=company_groups, permission__codename=permission_codename, content_type__model='action')
            if not all_action_permissions:
                return error_response(message=f"You are not authorized to perform the action: {action_name}")

            action_ids = list(all_action_permissions.values_list('object_pk', flat=True))
            has_permission = Action.objects.filter(pk__in=action_ids, title=action_name, process_id=process_id).last()
            if not has_permission:
                return error_response(message=f"You are not authorized to perform the action: {action_name}")
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator

