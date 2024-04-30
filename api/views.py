from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    VendorPerformanceSerializer
    )
from django.shortcuts import get_object_or_404

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import Vendor, PurchaseOrder,calculate_average_response_time

from datetime import datetime

class VendorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations for vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations for purchase orders.
    """

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def vendor_performance(request, vendor_id):
    """
    API endpoint that retrieves the performance data of a vendor.

    Method:
    GET

    Parameters:
    - `vendor_id` (required): The ID of the vendor.

    Request:
    - Headers:
        - `Authorization`: Token <user_token>

    Response:
    - Status code: 200 (OK) if successful retrieval, 404 (Not Found) if the vendor does not exist.

    Successful Response Content:
    {
        "on_time_delivery_rate": 0.95,
        "quality_rating_avg": 4.2,
        "average_response_time": 2.3,
        "fulfillment_rate": 0.98
    }

    Unsuccessful Response Content:
    {
        "detail": "Vendor not found."
    }

    Example:
    GET /api/vendor-performance/1/

    Successful Response:
    {
        "on_time_delivery_rate": 0.95,
        "quality_rating_avg": 4.2,
        "average_response_time": 2.3,
        "fulfillment_rate": 0.98
    }

    Unsuccessful Response:
    {
        "detail": "Vendor not found."
    }
    """

    vendor = get_object_or_404(Vendor, id=vendor_id)
    serializer = VendorPerformanceSerializer(vendor)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    """
    API endpoint that allows the acknowledgement of a purchase order by the vendor.

    Method:
    POST

    Parameters:
    - `po_id` (required): The ID of the purchase order.

    Request:
    - Headers:
        - `Authorization`: Token <user_token>

    Response:
    - Status code: 200 (OK) if successful acknowledgment, 401 (Unauthorized) if access is denied.
    - Content: Acknowledgement message.

    Example:
    POST /api/acknowledge-purchase-order/1/

    Response:
    - Status code: 200 (OK) if successful acknowledgment, 401 (Unauthorized) if access is denied.

    Successful Response Content:
    {
        "message": "Purchase order acknowledged."
    }

    Unsuccessful Response Content:
    {
        "message": "Access denied."
    }

    Example:
    POST /api/acknowledge-purchase-order/1/

    Successful Response:
    {
        "message": "Purchase order acknowledged."
    }

    Unsuccessful Response:
    {
        "message": "Access denied."
    }
    """

    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if purchase_order.vendor.user != request.user:
        return Response(
            {'message': 'Access denied.'},
            status=status.HTTP_401_UNAUTHORIZED
            )

    purchase_order.acknowledgment_date = datetime.now()
    purchase_order.save()
    calculate_average_response_time(purchase_order.vendor)

    return Response({'message': 'Purchase order acknowledged.'},
    status=status.HTTP_202_ACCEPTED)