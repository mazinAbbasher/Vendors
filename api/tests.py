from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Vendor,PurchaseOrder

from django.contrib.auth.models import User

from django.utils import timezone

class VendorPerformanceViewTestCase(TestCase):
    def setUp(self):
                            
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.user = User.objects.create_user(
            username='testuser',
             password='testpassword'
             )
        self.token = Token.objects.create(user=self.user)
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
            )
        self.admin_user.is_staff = True
        self.admin_user.save()
    
    def test_vendor_performance_unauthorized(self):
       
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vendor_performance(self):
        
        self.client.login(username='admin', password='adminpassword')

        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data.keys()),
            {'on_time_delivery_rate', 'quality_rating_avg',
             'average_response_time', 'fulfillment_rate'}
        )

    def test_vendor_performance_vendor_not_found(self):

        self.client.login(username='admin', password='adminpassword')

        url = reverse('vendor-performance', args=[999])  # Non-existent vendor ID
        response = self.client.get(url)
       
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
             password='testpassword'
             )
        
        self.token = Token.objects.create(user=self.user)
        
        self.vendor = Vendor.objects.create(  
            user=self.user,          
            name="test",
            contact_details="test",
            address = "test"
            )
        
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor,
            order_date=timezone.now(),
            expected_delivery_date=timezone.now(),
            actual_delivery_date=timezone.now(),
            items=[],
            quantity=10,
            status='Pending',
            quality_rating=4.5,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now()
        )

    def test_acknowledge_purchase_order(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        url = reverse('acknowledge-purchase-order', args=[self.purchase_order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['message'], 'Purchase order acknowledged.')

    def test_acknowledge_purchase_order_unauthorized(self):
        
        url = reverse('acknowledge-purchase-order', args=[self.purchase_order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_acknowledge_purchase_order_purchase_order_not_found(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('acknowledge-purchase-order', args=[999]) 
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
