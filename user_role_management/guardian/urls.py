from django.urls import path
from user_role_management.guardian.apis.v1 import permission

urlpatterns = [

    path('user_object_permission/', permission.UserObjectPermissionsApi.as_view(), name="user_object_permissions"),
    path('user_object_permission/<int:user_object_permission_id>', permission.UserObjectPermissionApi.as_view(), name="user_object_permission"),

    path('group_object_permission/', permission.GroupObjectPermissionsApi.as_view(), name="group_object_permissions"),
    path('group_object_permission/<int:group_object_permission_id>', permission.GroupObjectPermissionApi.as_view(), name="group_object_permission"),

]
