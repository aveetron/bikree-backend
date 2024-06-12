from rest_framework import serializers


class BikreeBaseSerializer(serializers.Serializer):
    guid = serializers.CharField(required=False, source="guid.hex")
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    updated_at = serializers.DateTimeField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False)

    class Meta:
        abstract = True