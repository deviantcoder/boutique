from django.db import models
from uuid import uuid4
from products.models import Product
from users.models import Profile


class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.product.name


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items():
        pass
