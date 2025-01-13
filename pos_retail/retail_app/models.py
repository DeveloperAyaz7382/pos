# In retail_app/models.py, define your models
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver



class Item_Type(models.Model):
    type_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    type_name = models.CharField(max_length=100)
    type_description = models.TextField()

    def __str__(self):
        return self.type_name
    


class CompanyInfo(models.Model):
    company_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    company_name = models.CharField(max_length=255)  # Company name as a string
    company_contact = models.CharField(max_length=255)  # Company contact number
    company_email = models.EmailField(max_length=254)  # Email field for company contact
    company_address = models.TextField()  # Address of the company

    def __str__(self):
        return self.company_name  # Display company name when instance is printed
    
    
    
    
class SalesmanInfo(models.Model):
    salesman_id = models.AutoField(primary_key=True)
    salesman_name = models.CharField(max_length=255)
    salesman_contact = models.CharField(max_length=20)
    company = models.ForeignKey(
        CompanyInfo, 
        on_delete=models.CASCADE, 
        related_name='salesmen'
    )
    
    
    
    
class Products(models.Model):
    ITEM_STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    type_id = models.ForeignKey(Item_Type, on_delete=models.CASCADE)  # Link to ItemType
    company_id = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)  # Link to CompanyInfo
    item_status = models.IntegerField(choices=ITEM_STATUS_CHOICES, default=1)

    def __str__(self):
        return self.item_name
    
    
class Stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True)  # Auto-incrementing ID
    item = models.ForeignKey(Products, on_delete=models.CASCADE)  # Link to InventoryItem
    stock_quantity = models.IntegerField()  # Quantity in stock
    stock_unitprice = models.DecimalField(max_digits=10, decimal_places=2)  # Unit price
    salesman = models.ForeignKey(SalesmanInfo, on_delete=models.CASCADE)  # Link to Salesman
    stock_total_value = models.DecimalField(max_digits=15, decimal_places=2)  # Total value of the stock
    stock_entry_date = models.DateField(auto_now_add=True)  # Automatically set the entry date

    def save(self, *args, **kwargs):
        # Automatically calculate the total value based on quantity and unit price
        self.stock_total_value = self.stock_quantity * self.stock_unitprice
        super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return f"Stock ID {self.stock_id} - {self.item.item_name} by {self.salesman.salesman_name}"
    
    
    # StockTracking model
class StockTracking(models.Model):
    tracking_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    item = models.ForeignKey(Products, on_delete=models.CASCADE)  # ForeignKey for item_id
    tracking_stock_in = models.IntegerField(default=0)  # Stock added
    tracking_stock_out = models.IntegerField(default=0)  # Stock removed
    tracking_current_stock = models.IntegerField()  # Current stock
    tracking_transaction_date = models.DateTimeField(default=now)  # Transaction date
    tracking_remarks = models.TextField(null=True, blank=True)  # Optional remarks

    def __str__(self):
        return f"Item {self.item.item_name} - {self.tracking_transaction_date}"
    
    
    
class StockExpiry(models.Model):
    expiry_id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)  # ForeignKey reference to InventoryItem
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    quantity_expiry = models.BigIntegerField()
    expiry_status = models.IntegerField(default=1)

    def __str__(self):
        return f"Expiry record for {self.item.item_name} - Expiry Date: {self.expiry_date}"
    
    
    
class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    order_customer_name = models.CharField(max_length=255)  # Customer name
    order_date = models.DateTimeField()  # Date and time of the order
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total order amount
    order_payment_status = models.CharField(max_length=50)  # Payment status (e.g., 'Paid', 'Pending')
    order_status = models.CharField(max_length=50)  # Order status (e.g., 'Completed', 'Cancelled')
    order_remarks = models.TextField()  # Remarks for the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the order was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the order was last updated

    def __str__(self):
        return f"Order #{self.order_id} - {self.order_customer_name}"
    
    
class OrderItem(models.Model):
    order_item_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_item_quantity = models.PositiveIntegerField()
    order_item_unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"OrderItem {self.order_item_id} for Order {self.order_id}"
    
    
    
class Wastage(models.Model):
    DAMAGE = 'Damage'
    SPOILAGE = 'Spoilage'
    EXPIRATION = 'Expiration'
    OTHER = 'Other'

    WASTAGE_REASONS = [
        (DAMAGE, 'Damage'),
        (SPOILAGE, 'Spoilage'),
        (EXPIRATION, 'Expiration'),
        (OTHER, 'Other'),
    ]

    PENDING = 'Pending'
    APPROVED = 'Approved'
    RETURNED = 'Returned'

    RETURN_STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (RETURNED, 'Returned'),
    ]

    # Set `wastage_id` as the primary key
    wastage_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()  # Number of items ordered
    quantity_received = models.PositiveIntegerField()  # Actual quantity received
    quantity_wasted = models.PositiveIntegerField()  # Quantity of items wasted
    reason_for_wastage = models.CharField(max_length=50, choices=WASTAGE_REASONS)  # Reason for wastage
    date_of_wastage = models.DateTimeField(auto_now_add=True)  # Date when wastage was identified
    return_status = models.CharField(max_length=50, choices=RETURN_STATUS, default=PENDING)  # Return status
    remarks = models.TextField(blank=True, null=True)  # Additional remarks

    def __str__(self):
        return f'{self.quantity_wasted} units of {self.item.item_name} wasted (ID: {self.wastage_id})'


