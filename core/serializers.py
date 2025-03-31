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
    scan = serializers.PrimaryKeyRelatedField(queryset=Scan.objects.all())

    class Meta:
        model = Check
        fields = "__all__"


class FindingSerializer(serializers.ModelSerializer):
    """Serializer for the Finding model."""
    parent_check = serializers.PrimaryKeyRelatedField(queryset=Check.objects.all())
    parent_check_details = CheckSerializer(source="parent_check", read_only=True)

    class Meta:
        model = Finding
        fields = "__all__"
