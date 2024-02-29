from django.urls import path
from user_role_management.manage.apis.v1 import user, process_action, company, organization_chart, permission

urlpatterns = [
    path('user/', user.UsersApi.as_view(), name="users"),
    path('user/<int:user_id>', user.UserApi.as_view(), name="user"),

    path('company/', company.CompaniesApi.as_view(), name="companies"),
    path('company/<int:company_id>', company.CompanyApi.as_view(), name="company"),

    path('group/', company.GroupsApi.as_view(), name="groups"),
    path('group/<int:group_id>', company.GroupApi.as_view(), name="group"),

    path('company_group/', company.CompanyGroupsApi.as_view(), name="company_groups"),
    path('company_group/<int:company_group_id>', company.CompanyGroupApi.as_view(), name="company_group"),

    path('permission/', permission.PermissionsApi.as_view(), name="permissions"),
    path('permission/<int:permission_id>', permission.PermissionApi.as_view(), name="permission"),

    path('employee/', organization_chart.EmployeesApi.as_view(), name="employees"),
    path('employee/<int:employee_id>', organization_chart.EmployeeApi.as_view(), name="employee"),

    path('position/', organization_chart.PositionsApi.as_view(), name="positions"),
    path('position/<int:position_id>', organization_chart.PositionApi.as_view(), name="position"),

    path('department/', organization_chart.DepartmentsApi.as_view(), name="departments"),
    path('department/<int:department_id>', organization_chart.DepartmentApi.as_view(), name="department"),

    path('company_department/', organization_chart.CompanyDepartmentsApi.as_view(), name="company_departments"),
    path('company_department/<int:company_department_id>', organization_chart.CompanyDepartmentApi.as_view(), name="company_department"),

    path('company_department_employee/', organization_chart.CompanyDepartmentEmployeesApi.as_view(), name="company_department_employees"),
    path('company_department_employee/<int:company_department_employee_id>', organization_chart.CompanyDepartmentEmployeeApi.as_view(), name="company_department_employee"),

    path('process/', process_action.ProcessesApi.as_view(), name="processes"),
    path('process/<int:process_id>', process_action.ProcessApi.as_view(), name="process"),

    path('action/', process_action.ActionsApi.as_view(), name="actions"),
    path('action/<int:action_id>', process_action.ActionApi.as_view(), name="action"),

]
