# ----- models.py ------

from django.db import models
from products.models import Product
from uuid import uuid4
from users.models import Profile

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    is_ordered = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['-product.title']

    def get_item_price(self):
        return int(product.price * quantity)

    def __str__(self):
        return f'{self.product.title}: {self.order_set.first}'


class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    items = models.ManyToManyField(OrderItem)

    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)
    
    ref_code = models.IntegerField(default=1, max_digits=15)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['-owner']

    def get_cart_items(self):
        return items.objects.all()

    def get_cart_total(self):
        return sum([item.get_item_price() for item in self.items.all()])

    def __str__(self):
        return f'{self.owner}: {self.ref_code}'


# ----- views.py -----

from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from .utils import ref_code_generator
from django.db.models import F

def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    
    if order.exists():
        return order[0]
    return 0 

@login_required(login_url='login_user')
def order_details(request):
    order = get_user_pending_order(request)
    context = {
        'order': order,
    }
    return render(request, 'cart/order_details.html', context)

@login_required(login_url='login_user')
def add_to_cart(request, pk):
    user_profile = get_object_or_404(Profile, user=request.user)

    product = get_object_or_404(Product, id=pk)
    item = OrderItem.objects.create(product=product)

    order, status = OrderItem.objects.get_or_create(owner=user_profile, is_ordered=False)

    if status:
        order.ref_code = ref_code_generator()
        order.save()

    return redirect('products')

@login_required(login_url='login_user')
def delete_from_cart(request, pk):
    item = OrderItem.objects.filter(id=pk)
    if item.exists():
        item[0].delete()
    return redirect('cart:order_details')

@login_required(login_url='login_user')
def increase_item_quantity(request, pk):
    item = OrderItem.objects.filter(id=pk).first()

    item.quantity = F('quantity') + 1
    item.save()

    return redirect('cart:order_details')


@login_required(login_url='login_user')
def decrease_item_quantity(request, pk):
    item = OrderItem.objects.filter(id=pk).first()

    if item.quantity > 1:
        item.quantity = F('quantity') - 1
        item.save()
        return redirect('cart:order_details')
    
    # flash message
    return redirect('cart:order_details')

# ----- signals.py -----

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Order

@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    try:
        for item in instance.get_cart_items():
            item.delete()
    except instance.DoesNotExist:
        pass

# ----- utils.py -----

import datetime
import string
import random

def ref_code_generator():
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M")[2:]
    rand_str = ''.join([random.choice(string.digits) for i in range(3)])

    return date_str + rand_str

# ----- products/templatetags/cart_filter.py -----

from django import tempate

register = template.Library()

@register.filter
def cart_filter(product, user):
    return product.is_in_cart(user)

# ----- products/models.py -----

class Product(models.Model):
    # ...
    def is_in_cart(self, user):
        return user.profile.order_set.first().items.filter(product=self).exists()

# ----- urls.py ----- 