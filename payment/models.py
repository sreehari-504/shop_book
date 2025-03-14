from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    # Don't pluralize the following
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipping_details = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)
    
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order- {str(self.id)}'

class OrderItem(models.Model):
    order_id = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  

    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f'Order Item - {str(self.id)}'