from django.contrib import admin
from user_role_management.users import models
from user_role_management.guardian.admin import GuardedModelAdmin
from user_role_management.guardian.shortcuts import get_objects_for_user, assign_perm
from user_role_management.guardian.models import GroupObjectPermission, UserObjectPermission


@admin.register(GroupObjectPermission)
class GroupObjectPermissionAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(models.BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'type', 'is_staff', 'is_active']
    list_editable = ['type', 'is_active']
    list_display_links = ['id', 'email']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['email'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        return form


@admin.register(models.Company)
class CompanyAdmin(GuardedModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


@admin.register(models.CompanyGroups)
class BaseGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'group']

    filter_horizontal = ("permissions",)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs["queryset"] = qs.select_related("content_type")
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


@admin.register(models.Process)
class ProcessAdmin(GuardedModelAdmin):
    list_display = ['id', 'name', 'created_by', 'is_deleted', 'company']
    list_display_links = ['id', 'name']


@admin.register(models.Route)
class RouteAdmin(GuardedModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']