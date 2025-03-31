import uuid

from django.db import models

from .constants import Constants


class Scan(models.Model):
    """
    Represents a Prowler scan session.
    """
    STATUS_CHOICES = (
        (Constants.PENDING.value, 'Pending'),
        (Constants.INPROGRESS.value, 'In Progress'),
        (Constants.COMPLETED.value, 'Completed'),
        (Constants.FAILED.value, 'Failed')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=Constants.PENDING.value)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Scan {self.id} - {self.status}"


class Check(models.Model):
    """
    Represents a check performed as part of a scan.
    """
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='checks')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_time = models.DateTimeField()
    related_url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('scan', 'uid')

    def __str__(self):
        return f"{self.uid} (Scan {self.scan.id})"


class Finding(models.Model):
    """
    Represents the findings of a check during a scan.
    """
    parent_check = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='findings')  # avoid naming conflict

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    status_code = models.CharField(max_length=50)
    status_detail = models.TextField()
    remediation_desc = models.TextField()
    remediation_references = models.JSONField(default=list)
    risk_details = models.TextField()
    created_time = models.DateTimeField()
    resources = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Finding {self.uid} (Check {self.parent_check.uid})"
