from django_filters import (CharFilter, FilterSet)
from django.contrib.postgres.search import SearchVector
from user_role_management.manage.models import Process, Action


class ProcessFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("name", "company")).filter(search=value)

    class Meta:
        model = Process
        fields = ('name', 'company_id', 'created_by', 'is_deleted')


class ActionFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector('name', 'code_name')).filter(search=value)

    class Meta:
        model = Action
        fields = ('name', 'code_name')

