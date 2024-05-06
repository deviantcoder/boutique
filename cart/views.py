from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from users.models import Profile
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from .utils import generate_order_id
from django.db.models import F


def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)

    if order.exists():
        return order[0]
    return 0


@login_required(login_url='login_user')
def order_details(request):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }

    return render(request, 'cart/order_details.html', context)


@login_required(login_url='login_user')
def add_to_cart(request, pk):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Product.objects.get(id=pk)

    order_item = OrderItem.objects.create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)

    user_order.items.add(order_item)

    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()

    return redirect('products')


@login_required(login_url='login_user')
def delete_from_cart(request, pk):
    item = OrderItem.objects.filter(id=pk)
    if item.exists():
        item[0].delete()
    return redirect('cart:order_details')


@login_required(login_url='login_user')
def increase_quantity(request, pk):
    order = get_user_pending_order(request)
    item = order.items.filter(id=pk).first()

    item.quantity = F("quantity") + 1
    item.save()

    return redirect('cart:order_details')


@login_required(login_url='login_user')
def decrease_quantity(request, pk):
    order = get_user_pending_order(request)
    item = order.items.all().first()

    if item.quantity > 1:
        item.quantity = F("quantity") - 1
        item.save()
        return redirect('cart:order_details')
    else:
        # add flash message that you cannot buy 0 items
        return redirect('cart:order_details')


@login_required(login_url='login_user')
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, '', context)



def cart(request):
    context = {}

    return render(request, 'cart/order_summary.html', context)
