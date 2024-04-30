from django.urls import path, include
from rest_framework import routers
from .views import VendorViewSet, PurchaseOrderViewSet,vendor_performance,acknowledge_purchase_order

router = routers.DefaultRouter()
router.register('vendors', VendorViewSet)
router.register('purchase-orders', PurchaseOrderViewSet)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance', vendor_performance,name="vendor-performance"),
    path('purchase_orders/<int:po_id>/acknowledge', acknowledge_purchase_order,name="acknowledge-purchase-order"),
]
