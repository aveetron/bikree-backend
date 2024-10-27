from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
  class Meta:
    fields = "__all__"
    model = "Order"


class OrderDetailSerializer(serializers.Serializer):
  class Meta:
    fields = "__all__"
    model = "OrderDetail"