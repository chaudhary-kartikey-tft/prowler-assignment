
import django_filters


class ScanFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")


class CheckFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")


class FindingFilter(django_filters.FilterSet):
    severity = django_filters.CharFilter(field_name="severity", lookup_expr="exact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    status_code = django_filters.CharFilter(field_name="status_code", lookup_expr="exact")
