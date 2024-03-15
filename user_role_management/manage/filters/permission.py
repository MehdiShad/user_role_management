from django.contrib.auth.models import Permission
from django_filters import (CharFilter, FilterSet)
from django.contrib.postgres.search import SearchVector


class PermissionFilter(FilterSet):
    search = CharFilter(method='filter_search', lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("name", "codename")).filter(search=value)

    class Meta:
        model = Permission
        fields = ('name', 'content_type_id', 'codename')
