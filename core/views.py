from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .filters import CheckFilter, FindingFilter, ScanFilter
from .models import Check, Finding, Scan
from .pagination import CustomPagination
from .serializers import CheckSerializer, FindingSerializer, ScanSerializer
from .tasks import initiate_prowler_scan


class ScanViewSet(viewsets.ModelViewSet):
    """
    Scan viewset for listing, creating, updating, retrieving and deleting scans.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ScanFilter
    ordering_fields = ['started_at']
    ordering = ['-started_at']

    def create(self, request, *args, **kwargs):
        """Start a new scan using given AWS credentials"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.save()
        initiate_prowler_scan.delay(str(serializer_data.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckViewSet(viewsets.ModelViewSet):
    """
    Check viewset for listing, creating, updating, retrieving and deleting checks.
    """
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CheckFilter
    ordering_fields = ['created_time']
    ordering = ['-created_time']

    def get_queryset(self):
        """
        Filter checks queryset based on scan_id.
        """
        scan_id = self.kwargs.get('scan_pk')
        queryset = self.queryset.filter(scan_id=scan_id)
        return queryset


class FindingViewSet(viewsets.ModelViewSet):
    """
    Finding viewset for listing, creating, updating, retrieving and deleting findings.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FindingFilter
    ordering_fields = ['created_time']
    ordering = ['-created_time']

    def get_queryset(self):
        """
        Filter findings queryset based on scan_id.
        If check_id present in query_params, also filters based on that.
        """
        scan_id = self.kwargs.get('scan_pk')
        queryset = self.queryset.filter(parent_check__scan_id=scan_id)

        check_id = self.request.query_params.get('check_id')
        if check_id:
            queryset = queryset.filter(parent_check_id=check_id)
        return queryset
