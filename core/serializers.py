from rest_framework import serializers

from .models import Scan, Check, Finding


class ScanSerializer(serializers.ModelSerializer):
    """Serializer for the Scan model."""

    class Meta:
        model = Scan
        fields = "__all__"

    def to_representation(self, instance):
        # Get the latest status before serializing
        instance.refresh_from_db()
        return super().to_representation(instance)


class CheckSerializer(serializers.ModelSerializer):
    """Serializer for the Check model."""
    scan = ScanSerializer()

    class Meta:
        model = Check
        fields = "__all__"


class FindingSerializer(serializers.ModelSerializer):
    """Serializer for the Finding model."""
    parent_check = CheckSerializer()

    class Meta:
        model = Finding
        fields = "__all__"
