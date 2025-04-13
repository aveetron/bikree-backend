from rest_framework.viewsets import ViewSet
from rest_framework import status

from core.http_utils import HttpUtil
from core.permissions import IsSalesRepresentative, IsShopOwner
from .models import Order
from .serializers import OrderDetailSerializer, OrderSerializer


class OrderApi(ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsSalesRepresentative]
    lookup_field = "uid"

    def list(self, request):
        try:
            orders = Order.objects.filter(created_by=request.user)
            if request.query_params.get("order_no", None):
                orders = orders.filter(order_no=request.query_params.get("order_no"))
            elif request.query_params.get("status", None):
                orders = orders.filter(is_paid=request.query_params.get("status"))
            elif request.query_params.get("from_date", None) and request.query_params.get("to_date", None):
                orders = orders.filter(created_at__range=[request.query_params.get("from_date"), request.query_params.get("to_date")])
            elif request.query_params.get("is_paid", None):
                orders = orders.filter(is_paid=request.query_params.get("is_paid"))
            else:
                pass

            # serialize those data
            serializer = self.serializer_class(orders, many=True)
            return HttpUtil.success_response(orders, serializer.data)
        except Exception as e:
            return HttpUtil.error_response(message=e.args[0])
        
    def create(self, request):
        try:
            order_serializer = self.serializer_class(data=request.data)
            if not order_serializer.is_valid():
                return HttpUtil.error_response(message=order_serializer.errors)
            order_serializer.save(created_by=request.user)

            order_detail_serializer = OrderDetailSerializer(data=request.data["order_details"], many=True)
            if not order_detail_serializer.is_valid():
                return HttpUtil.error_response(message=order_detail_serializer.errors)
            order_detail_serializer.save(order=order_serializer.data)   
            return HttpUtil.success_response(message="Order Created", code=status.HTTP_201_CREATED)
        except Exception as e:
            return HttpUtil.error_response(message=e.args[0])
        
    def retrieve(self, request, uid=None):
        try:
            order = Order.objects.get(uid=uid)
            return HttpUtil.get_response(order, OrderSerializer)
        except Exception as e:
            return HttpUtil.error_response(message=e.args[0])

    def update(self, request, uid=None):
        try:
            order = Order.objects.get(uid=uid, status=False)
            if not order:
                return HttpUtil.error_response(message="Order Not Found", code=status.HTTP_404_NOT_FOUND)   
            order_serializer = OrderSerializer(order, data=request.data)
            if not order_serializer.is_valid():
                return HttpUtil.error_response(message=order_serializer.errors)
            order_serializer.save()
            return HttpUtil.success_response(message="Order Updated", code=status.HTTP_200_OK)
        except Exception as e:
            return HttpUtil.error_response(message=e.args[0])

    def delete(self, request, uid=None):
        try:
            order = Order.objects.get(uid=uid)
            order.delete()
            return HttpUtil.success_response(message="Order Deleted", code=status.HTTP_200_OK)
        except Exception as e:  
            return HttpUtil.error_response(message=e.args[0])
    

class ApproveOrderApi(ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsShopOwner]
    lookup_field = "uid"

    def partial_update(self, request, uid=None):
        try:
            order = Order.objects.get(uid=uid, status=False)
            if not order:
                return HttpUtil.error_response(message="Order Not Found", code=status.HTTP_404_NOT_FOUND)   
            # change the status for making this order approved
            order.status = True
            order.save()
            return HttpUtil.success_response(message="Order Updated", code=status.HTTP_200_OK)
        except Exception as e:
            return HttpUtil.error_response(message=e.args[0])