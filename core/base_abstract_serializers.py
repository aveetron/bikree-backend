from rest_framework import serializers


class BikreeBaseSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, source="uid.hex")
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    updated_at = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        abstract = True


class BikreeBaseModelSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True, source="uid.hex")

    class Meta:
        abstract = True
