from typing import Dict, Literal
from django.http import HttpRequest
from django.db.models import QuerySet
from rest_framework import serializers
from django.contrib.auth.models import Permission, ContentType
from user_role_management.manage.filters import permission as permission_filters
from user_role_management.core.exceptions import error_response, success_response
from user_role_management.manage.models import Company, Company_group, Action, Process
from user_role_management.utils.serializer_handler import CustomMultiResponseSerializerBase
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission


def get_permissions(request, **kwargs) -> QuerySet[Permission]:
    return Permission.objects.all()


def get_filtered_permissions(request: HttpRequest, filters=None) -> QuerySet[Permission]:
    filters = filters or {}
    qs = Permission.objects.all().order_by('-id')
    return permission_filters.PermissionFilter(filters, qs).qs


def get_permission(request: HttpRequest, id: int) -> Dict[str, Literal['is_success', True, False]]:
    try:
        group = Permission.objects.get(id=id)
        return success_response(data=group)
    except Exception as ex:
        return error_response(message="There are no record")


def get_user_permissions(request: HttpRequest) -> Dict[str, Literal['is_success', True, False]]:
    try:
        user = request.user
        last_company_id = user.last_company_logged_in_id
        user_permissions = user.user_permissions.all()
        process_model_id = ContentType.objects.get(model='process')
        action_model_id = ContentType.objects.get(model='action')

        company_groups = user.company_groups.all()
        access_processes = GroupObjectPermission.objects.filter(content_type_id__in=[process_model_id.id],
                                                                group_id__in=company_groups)
        access_actions = GroupObjectPermission.objects.filter(content_type__in=[action_model_id.id],
                                                              group_id__in=company_groups)
        access_processes_ids = list(access_processes.values_list('object_pk', flat=True))
        access_actions_ids = list(access_actions.values_list('object_pk', flat=True))
        all_processes = Process.objects.filter(pk__in=access_processes_ids, company_id=last_company_id)
        all_processes_ids = all_processes.values_list('id', flat=True)
        all_actions = Action.objects.filter(process_id__in=all_processes_ids, pk__in=access_actions_ids)
        sd = UserObjectPermission.objects.filter(user_id=user.id)
        sdd = GroupObjectPermission.objects.filter(group_id__in=company_groups)
        response = {
            'is_success': True,
            'access_processes': all_processes,
            'access_actions': all_actions,
        }
        return response
    except Exception as ex:
        return error_response(message=str(ex))
