from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import CheckViewSet, FindingViewSet, ScanViewSet

router = DefaultRouter()
router.register(r'scans', ScanViewSet, basename='scans')

scan_checks_router = NestedDefaultRouter(router, r'scans', lookup='scan')
scan_checks_router.register(r'checks', CheckViewSet, basename='scan-checks')

scan_findings_router = NestedDefaultRouter(router, r'scans', lookup='scan')
scan_findings_router.register(r'findings', FindingViewSet, basename='scan-findings')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(scan_checks_router.urls)),
    path('', include(scan_findings_router.urls)),
]
