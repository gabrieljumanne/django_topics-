from django.db import models
from django.utils import timezone
from datetime import date, time, timedelta

# E-commerce order management system 

#customer model 

class Customer(models.Model):
    name = models.CharField("Customer name", max_length=100)
    email = models.EmailField("customer emaiL", unique=True)
    phone = models.CharField("Contact", max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
# product model 

class Product(models.Model):
    name = models.CharField("product name", max_length=100)
    description = models.TextField("description", )
    price = models.DecimalField("product price", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Stocks", )
    created_at = models.DateTimeField("Date created", auto_now_add=True)
    
    def __str__(self):
        return self.name
    
# oder model manager with custom query 

class OrderManager(models.Manager):
    def within_date_range(self, start_date, end_date):
        """ Retrive order within specific range"""
        return self.filter(created_at__range=(start_date, end_date))
    
    def high_value_orders(self, min_total):
        "retrieve orders that their values is above minimum values"
        return self.filter(total_price__gte=min_total)
    
    def by_status(self, status):
        "retrieve order by with the certain status"
        return self.filter(status=status)
    
    def for_customer(self, customer_id):
        """retrieve order for the particular customer"""
        return self.filter(customer_id = customer_id)
    
# order model
class Order(models.Model):
    STATUS_CHOICE = [
        ('pending', 'pending'),
        ('processing', 'processing'), 
        
        ('complete', 'complete'),
        ('canceled', 'canceled')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_orders" )
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField("Order status", max_length=20, choices=STATUS_CHOICE, default="pending")
    created_at = models.DateTimeField("oder creation time", auto_now_add=True, )
    total_price = models.DecimalField("Total price", max_digits=10, decimal_places=2, default = 0.00)
    
    # custom oder manager to manage all the the orders ...  
    orders = OrderManager()
    objects = models.Manager()
    
    def __str__(self):
        return f"Oder {self.id} by {self.customer.name}"
        
        
# inter- class for the ordering 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE, )
    # custom oder manager to manage all
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("quantity", )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"