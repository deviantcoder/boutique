from django.db import models
from uuid import uuid4
from products.models import Product
from users.models import Profile


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True)

    is_ordered = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['product']

    def __str__(self) -> str:
        return f'{self.product.title} - {self.order_set.first()}'


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def get_cart_items(self):
        return self.items.all()
    
    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])
    
    def __str__(self):
        return f'Order: {self.owner} - {self.ref_code}'
