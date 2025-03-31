from django.urls import re_path
from .consumers import ScanStatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/scans/(?P<scan_id>[a-f0-9\-]+)/status/$", ScanStatusConsumer.as_asgi()),
]
