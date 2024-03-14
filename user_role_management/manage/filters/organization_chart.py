from django_filters import (CharFilter, FilterSet)
from django.contrib.postgres.search import SearchVector
from django.db.models import Case, When, F, Value, IntegerField, QuerySet, DateField, Q
from user_role_management.manage.models import Company_position, Employee, Company_department, \
    Company_department_employee, Company_department_position


class CompanyPositionFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("title", "abbreviation")).filter(search=value)

    class Meta:
        model = Company_position
        fields = ('title', 'company_id', 'abbreviation')


class EmployeesFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("personnel_code")).filter(search=value)

    class Meta:
        model = Employee
        fields = ('personnel_code', 'company')


class CompanyDepartmentFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("department")).filter(search=value)

    class Meta:
        model = Company_department
        fields = ('department', 'company')


class CompanyDepartmentEmployeeFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("company_department")).filter(search=value)

    class Meta:
        model = Company_department_employee
        fields = ('company_department', )


class CompanyDepartmentPositionFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("company_department")).filter(search=value)

    class Meta:
        model = Company_department_position
        fields = ('company_department', )
