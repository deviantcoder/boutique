from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('products/', views.products_view, name='products'),
    path('product/<str:pk>/', views.product_view, name='product'),
    path('add-product/', views.add_product, name='add_product'),
    path('category/<str:pk>/', views.products_in_category, name='products_in_category'),
    path('subcategory/<str:pk>/', views.products_in_subcategory, name='products_in_subcategory'),
    path('collection/<str:pk>/', views.products_in_collection, name='collection'),
]
