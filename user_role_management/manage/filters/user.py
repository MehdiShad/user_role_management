from django_filters import (CharFilter, FilterSet)
from django.contrib.postgres.search import SearchVector
from user_role_management.manage.models import BaseUser
from django.db.models import Case, When, F, Value, IntegerField, QuerySet, DateField, Q


class UsersFilter(FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr="icontains")
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("email", "first_name", "last_name")).filter(search=value)

    class Meta:
        model = BaseUser
        fields = ('email', 'first_name', 'last_name', 'type')
