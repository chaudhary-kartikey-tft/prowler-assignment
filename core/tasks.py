import logging
import subprocess

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.utils import timezone

from .constants import Constants
from .models import Scan
from .utils import process_prowler_results

logger = logging.getLogger(__name__)


@shared_task
def initiate_prowler_scan(scan_id):
    """
    Runs a prowler scan asynchronously (through prowler cli and subprocess)
    """

    scan = Scan.objects.get(id=scan_id)
    scan.status = Constants.INPROGRESS.value
    scan.save()

    output_filename = f"prowler_scan_{scan_id}"
    prowler_command = [
        "prowler", "aws",
        "-M", "json-ocsf",
        "--output-filename", output_filename,
        "--output-directory", "/tmp"
    ]

    try:
        # Initiate prowler scan and capture its output and errors.
        # "check=False" is set so that no exception is raised when returning exit codes other than 0.
        result = subprocess.run(prowler_command, capture_output=True, text=True, check=False)
        logger.info(f"Prowler Output:\n{result.stdout}")
        logger.error(f"Prowler Errors:\n{result.stderr}")

        # subprocess exit-code 3 is returned when any security check fails, we don't mark the scan as failed
        if result.returncode == 3:
            logger.warning("Prowler found failed security checks, but scan completed successfully.")
        elif result.returncode != 0:
            logger.error(f"Prowler scan failed with exit code {result.returncode}")
            scan.status = Constants.FAILED.value
            scan.error_message = result.stderr
            scan.save()
            return

        scan.status = Constants.COMPLETED.value
        scan.ended_at = timezone.now()

        # Process scan results and save checks and findings for scan.
        process_prowler_results(scan, f"/tmp/{output_filename}.ocsf.json")
    except Exception as err:
        logger.error(f"Scan {scan_id} failed: {err}")
        scan.status = Constants.FAILED.value
        scan.error_message = str(err)
    finally:
        scan.save()
        # send websocket notification for status once scan is complete
        notify_scan_status(scan_id, scan.status)


def notify_scan_status(scan_id, status):
    """Send scan status update to WebSocket group."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"scan_{scan_id}",
        {"type": "scan_status_update", "status": status},
    )
