from .models import Product, Tag, Category, Subcategory
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_products(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    subcategories = Subcategory.objects.filter(name__icontains=search_query)

    products = Product.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags) |
        Q(category__name__icontains=search_query) |
        Q(subcategory__in=subcategories)
    )

    return products, search_query


def pagination(request, products, results):
    page = request.GET.get('page')
    paginator = Paginator(products, results)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    left_index = int(page) - 2
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 3
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return products, custom_range, paginator
