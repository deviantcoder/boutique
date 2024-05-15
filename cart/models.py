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

    def get_item_price(self):
        return int(self.product.price * self.quantity)

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
        return sum([item.get_item_price() for item in self.items.all()])
    
    def __str__(self):
        return f'Order: {self.owner} - {self.ref_code}'


class OrderCheckout(models.Model):
    PAYMENT_METHODS = (
        ('Cash on delivery', 'Cash on delivery'),
        ('Credit card', 'Credit card'),
        ('Google Pay', 'Google Pay'),
    )

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS, null=True)

    created = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return f'{self.user}: {self.country} - {self.city}'
    