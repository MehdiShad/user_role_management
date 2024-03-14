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

    path('company_branch/', company.CompanyBranchesApi.as_view(), name="company_branch"),
    path('company_branch/<int:company_branch_id>', company.CompanyBranchApi.as_view(), name="company_branch"),

    path('permission/', permission.PermissionsApi.as_view(), name="permissions"),
    path('permission/<int:permission_id>', permission.PermissionApi.as_view(), name="permission"),

    path('user_permissions/', permission.UserPermissionsApi.as_view(), name="user_permissions"),

    path('employee/', organization_chart.EmployeesApi.as_view(), name="employees"),
    path('employee/<int:employee_id>', organization_chart.EmployeeApi.as_view(), name="employee"),

    path('Company_position/', organization_chart.CompanyPositionsApi.as_view(), name="Company_positions"),
    path('Company_position/<int:Company_position_id>', organization_chart.CompanyPositionApi.as_view(), name="Company_position"),

    path('company_department/', organization_chart.CompanyDepartmentsApi.as_view(), name="company_departments"),
    path('company_department/<int:company_department_id>', organization_chart.CompanyDepartmentApi.as_view(), name="company_department"),

    path('company_department_employee/', organization_chart.CompanyDepartmentEmployeesApi.as_view(), name="company_department_employees"),
    path('company_department_employee/<int:company_department_employee_id>', organization_chart.CompanyDepartmentEmployeeApi.as_view(), name="company_department_employee"),

    path('company_department_position/', organization_chart.CompanyDepartmentPositionsApi.as_view(), name="company_department_positions"),
    path('company_department_position/<int:company_department_position_id>', organization_chart.CompanyDepartmentPositionApi.as_view(), name="company_department_position"),

    path('process/', process_action.ProcessesApi.as_view(), name="processes"),
    path('process/<int:process_id>', process_action.ProcessApi.as_view(), name="process"),

    path('action/', process_action.ActionsApi.as_view(), name="actions"),
    path('action/<int:action_id>', process_action.ActionApi.as_view(), name="action"),

]
