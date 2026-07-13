from rest_framework import serializers

from ports.models import PortCallCache


class PortCallCacheSerializer(serializers.ModelSerializer):
    portCall = serializers.CharField(source="port_unlocode", read_only=True)
    searchType = serializers.CharField(source="search_type", read_only=True)
    vesselType = serializers.CharField(source="vessel_type", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = PortCallCache
        fields = (
            "portCall",
            "searchType",
            "vesselType",
            "data",
            "createdAt",
            "updatedAt",
        )
