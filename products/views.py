from django.shortcuts import render, redirect
from .models import Product, ProductImage, Category, Subcategory, Collection, Review
from .utils import search_products, pagination
from .forms import ProductForm, ProductImageFormSet, ReviewForm
from django.db.models import Min, Max


def products_view(request):
    products, search_query = search_products(request)
    results = 12
    products, custom_range, paginator = pagination(request, products, results)

    categories = Category.objects.all()

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    context = {
        'products': products,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator,
        'categories': categories,
        'user': request.user,
        'min_max_price': min_max_price,
    }

    return render(request, 'products/products.html', context)


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    related_products = Product.objects.filter(category=product.category).exclude(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user.profile
            review.save()

            return redirect('product', pk=pk)

    product.get_vote_count()

    context = {
        'product': product,
        'related_products': related_products,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    form = ProductForm()
    formset = ProductImageFormSet()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()

            return redirect('product', pk=product.id)

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'products/product_form.html', context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', pk)
        
    context = {
        'form': form,
    }

    return render(request, 'products/product_form.html', context)


def delete_product(request):
    pass


def products_in_category(request, pk):
    page = 'pr_in_cat'  # products in category

    category = Category.objects.get(id=pk)
    categories = Category.objects.all()
    products = category.product_set.all()

    results = 12
    products, custom_range, paginator = pagination(request, products, results)
    
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    context = {
        'page': page,
        'category': category,
        'products': products,
        'categories': categories,
        'custom_range': custom_range,
        'paginator': paginator,
        'min_max_price': min_max_price,
    }

    return render(request, 'products/products_in_category.html', context)


def products_in_subcategory(request, pk):
    page = 'pr_in_sub'  # products in subcategory

    subcategory = Subcategory.objects.get(id=pk)
    category = subcategory.category
    categories = Category.objects.all()
    products = subcategory.product_set.all()

    products, custom_range, paginator = pagination(request, products, results=12)

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    context = {
        'page': page,
        'subcategory': subcategory,
        'category': category,
        'categories': categories,
        'products': products,
        'custom_range': custom_range,
        'paginator': paginator,
        'min_max_price': min_max_price,
    }

    return render(request, 'products/products_in_category.html', context)


def products_in_collection(request, pk):
    page = 'pr_in_col' # products in collection

    collection = Collection.objects.get(id=pk)

    products = collection.product_set.all()
    categories = Category.objects.all()

    context = {
        'collection': collection,
        'products': products,
        'categories': categories,   
        'page': page,
    }

    return render(request, 'products/products_in_category.html', context)


def home_page(request):
    categories = Category.objects.all()[:3]
    top_products = Product.objects.filter(votes_ratio__gte=2)[:4]
    collections = Collection.objects.all()

    context = {
        'categories': categories,
        'top_products': top_products,
        'collections': collections,
    }

    return render(request, 'products/home.html', context)
