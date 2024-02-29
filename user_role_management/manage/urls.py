from django.urls import path
from user_role_management.manage.apis.v1 import user, process_action, company, organization_chart

urlpatterns = [

    path('company/', company.CompaniesApi.as_view(), name="companies"),
    path('company/<int:company_id>', company.CompanyApi.as_view(), name="company"),

    path('employee/', organization_chart.EmployeesApi.as_view(), name="employees"),
    path('employee/<int:department_id>', organization_chart.EmployeeApi.as_view(), name="employee"),

    path('position/', organization_chart.PositionsApi.as_view(), name="positions"),
    path('position/<int:position_id>', organization_chart.PositionApi.as_view(), name="position"),

    path('department/', organization_chart.DepartmentsApi.as_view(), name="departments"),
    path('department/<int:department_id>', organization_chart.DepartmentApi.as_view(), name="department"),

    path('process/', process_action.ProcessesApi.as_view(), name="processes"),
    path('process/<int:process_id>', process_action.ProcessApi.as_view(), name="process"),

    path('action/', process_action.ActionsApi.as_view(), name="actions"),
    path('action/<int:action_id>', process_action.ActionApi.as_view(), name="actions"),

    path('register/', user.RegisterApi.as_view(), name="register"),
    # path('processes/', process_action.ProcessApi.as_view(), name="processes"),

]
