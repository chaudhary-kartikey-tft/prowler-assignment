import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Scan


class ScanStatusConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer that sends real-time scan status updates.
    """

    async def connect(self):
        self.scan_id = self.scope["url_route"]["kwargs"]["scan_id"]
        self.group_name = f"scan_{self.scan_id}"

        # Join scan-specific group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the group on disconnect."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming messages."""
        data = json.loads(text_data)
        action = data.get("action", "")

        if action == "fetch_status":
            scan = await sync_to_async(Scan.objects.get)(id=self.scan_id)
            await self.send(text_data=json.dumps({"status": scan.status}))

    async def scan_status_update(self, event):
        """Send scan status update to WebSocket client."""
        await self.send(text_data=json.dumps({"status": event["status"]}))
