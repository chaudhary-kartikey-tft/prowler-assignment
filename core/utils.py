import json
import logging

from dateutil import parser
from django.utils import timezone

from .models import Check, Finding

logger = logging.getLogger(__name__)


def process_prowler_results(scan, prowler_output_path):
    """
    Reads Prowler JSON output and saves Check and Finding data.
    """
    try:
        with open(prowler_output_path, "r") as file:
            prowler_data = json.load(file)

        for check_data in prowler_data:
            check_uid = check_data.get("metadata", {}).get("event_code", "unknown")

            created_time = check_data.get("finding_info", {}).get("created_time_dt")
            tz_aware_created_time = timezone.make_aware(parser.parse(created_time))
            # Create check if it doesn't already exist
            check, _ = Check.objects.get_or_create(
                scan=scan,
                uid=check_uid,
                defaults={
                    "title": check_data.get("finding_info", {}).get("title", "No Title"),
                    "description": check_data.get("finding_info", {}).get("desc", "No Description"),
                    "created_time": tz_aware_created_time,
                    "related_url": check_data.get("unmapped", {}).get("related_url", ""),
                }
            )

            # Process finding for this check
            created_time = check_data.get("time_dt")
            tz_aware_created_time = timezone.make_aware(parser.parse(created_time))
            Finding.objects.create(
                parent_check=check,
                uid=check_data.get("finding_info", {}).get("uid", "Unknown"),
                severity=check_data.get("severity", "Unknown"),
                status=check_data.get("status", "Unknown"),
                status_code=check_data.get("status_code", "Unknown"),
                status_detail=check_data.get("status_detail", ""),
                remediation_desc=check_data.get("remediation", {}).get("desc", ""),
                remediation_references=check_data.get("remediation", {}).get("references", []),
                risk_details=check_data.get("risk_details", ""),
                created_time=tz_aware_created_time,
                resources=check_data.get("resources", []),
            )

    except Exception as e:
        logger.error(f"Error processing Prowler results: {e}")
