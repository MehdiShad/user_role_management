from django_filters import (CharFilter, FilterSet)
from user_role_management.manage.models import Company
from django.contrib.postgres.search import SearchVector
from django.db.models import Case, When, F, Value, IntegerField, QuerySet, DateField, Q


class CompanyFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("title")).filter(search=value)

    class Meta:
        model = Company
        fields = ('title',)
