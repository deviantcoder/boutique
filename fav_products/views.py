from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile
from .models import FavItem, FavoriteProducts
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.db.models import Q
from django.contrib import messages


def get_user_fav_products(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    fav_products = FavoriteProducts.objects.filter(owner=user_profile)

    if fav_products.exists():
        return fav_products[0]
    return 0


@login_required(login_url='login_user')
def fav_products_details(request):
    fav_products = get_user_fav_products(request)
    context = {
        'fav_products': fav_products,
    }
    return render(request, 'fav_products/fav_products.html', context)


@login_required(login_url='login_url')
def add_to_fav(request, pk):
    user_profile = get_object_or_404(Profile, user=request.user)
    fav_products, status = FavoriteProducts.objects.get_or_create(owner=user_profile)

    product = Product.objects.get(id=pk)
    item = FavItem.objects.create(product=product)

    fav_products.items.add(item)

    messages.success(request, 'Item was added to wishlist')

    return redirect(request.GET['next'] if 'next' in request.GET else 'products')


@login_required(login_url='login_url')
def delete_from_fav(request, pk):
    item = FavItem.objects.filter(
        Q(product__id=pk) |
        Q(id=pk)
        )
    if item.exists():
        item[0].delete()

        messages.info(request, 'Item was deleted from wishlist')

        return redirect(request.GET['next'] if 'next' in request.GET else 'fav_products')

    return redirect('fav_products')
