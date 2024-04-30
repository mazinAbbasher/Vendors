from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save,pre_save
from django.db.models import Avg, F

from django.dispatch import receiver

from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True,default = None)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField(null=True)
    actual_delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()  

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        calculate_on_time_delivery_rate(instance.vendor)

    if instance.status == 'completed' and instance.quality_rating is not None:
        calculate_quality_rating_avg(instance.vendor)


@receiver(pre_save, sender=PurchaseOrder)
def update_vendor_metrics_on_status_change(sender, instance, **kwargs):
    if instance.pk: 
        original_status = sender.objects.get(pk=instance.pk).status
        if original_status != instance.status:
            calculate_fulfillment_rate(instance.vendor)

def calculate_on_time_delivery_rate(vendor):
    completed_purchase_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        expected_delivery_date__isnull=False,
    )
    on_time_delivery_count = completed_purchase_orders.filter(
        actual_delivery_date__lte=models.F('expected_delivery_date')
    ).count()
    total_completed_count = completed_purchase_orders.count()

    if total_completed_count > 0:
        vendor.on_time_delivery_rate = on_time_delivery_count / total_completed_count
    else:
        vendor.on_time_delivery_rate = None
    vendor.save()

def calculate_quality_rating_avg(vendor):
    completed_purchase_orders_with_rating = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        quality_rating__isnull=False,
    )
    quality_rating_avg = completed_purchase_orders_with_rating.aggregate(
        avg_rating=Avg('quality_rating')
    )['avg_rating']

    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()

def calculate_average_response_time(vendor):
    acknowledged_purchase_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        acknowledgment_date__isnull=False
    )
    response_time_avg = acknowledged_purchase_orders.aggregate(
            avg_duration=Avg(F('acknowledgment_date') - F('issue_date'))
        )['avg_duration']
    if response_time_avg:
        vendor.average_response_time = response_time_avg.total_seconds()
    else:
        vendor.average_response_time = 0
    vendor.save()

def calculate_fulfillment_rate(vendor):
    total_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    completed_purchase_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
    ).count()

    if total_purchase_orders > 0:
        vendor.fulfillment_rate = completed_purchase_orders / total_purchase_orders
    else:
        vendor.fulfillment_rate = None

    vendor.save()