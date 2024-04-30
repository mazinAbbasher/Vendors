# Vendor management system


To install and run, follow these steps:

1. Clone the repository
2. Navigate to the project directory
3. install pipenv on your device, run "pip install pipenv"
4. run "pipenv shell"
5. run "pipenv install"
6. run "python manage.py migrate"
7. run "python manage.py createsuperuser" and create super user with name and password(remember them)
8. run "pythonn manage.py runserver"
9. open your browser at 127.0.01:8000/api/
10. you will see the rest_framework interface
11. UnAuthorized, click on login button at top right and use your superuser credentials
12. congrats, you can use this system now.

# Testing
To test this system just run "python manage.py test"

the vendor_performance and acknowledge_purchase_order endpoint will be tested with several scenarios, there is no any test for vendor and purchase_order views because i just used rest_framework viewset without any modification or customization. 


#API Documentation

1. VendorViewSet

API endpoint that allows CRUD operations for vendors.
Endpoint

/api/vendors/


2. PurchaseOrderViewSet

API endpoint that allows CRUD operations for purchase orders.
Endpoint

/api/purchase-orders/


3. Vendor Performance

API endpoint that retrieves the performance data of a vendor.
Endpoint

/api/vendors/<int:vendor_id>/performance

Methods

    GET: Retrieves the performance data of a vendor.

Parameters

    vendor_id (required): The ID of the vendor.

Request Headers

    Authorization: Token <user_token>

Response

    Status code: 200 (OK) if successful retrieval, 404 (Not Found) if the vendor does not exist.

Successful Response Content
json

{
    "on_time_delivery_rate": 0.95,
    "quality_rating_avg": 4.2,
    "average_response_time": 2.3,
    "fulfillment_rate": 0.98
}

Unsuccessful Response Content
json

{
    "detail": "Vendor not found."
}

Example

GET /api/vendor-performance/1/

Successful Response
json

{
    "on_time_delivery_rate": 0.95,
    "quality_rating_avg": 4.2,
    "average_response_time": 2.3,
    "fulfillment_rate": 0.98
}

Unsuccessful Response
json

{
    "detail": "Vendor not found."
}

4. Acknowledge Purchase Order

API endpoint that allows the acknowledgement of a purchase order by the vendor.
Endpoint

/api/purchase_orders/<int:po_id>/acknowledge

Methods

    POST: Acknowledges a purchase order.

Parameters

    po_id (required): The ID of the purchase order.

Request Headers

    Authorization: Token <user_token>

Response

    Status code: 200 (OK) if successful acknowledgment, 401 (Unauthorized) if access is denied.
    Content: Acknowledgement message.

Successful Response Content
json

{
    "message": "Purchase order acknowledged."
}

Unsuccessful Response Content
json

{
    "message": "Access denied."
}

Example

POST /api/acknowledge-purchase-order/1/

Successful Response
json

{
    "message": "Purchase order acknowledged."
}

Unsuccessful Response
json

{
    "message": "Access denied."
}

