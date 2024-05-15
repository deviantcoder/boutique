from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('order-details/', views.order_details, name='order_details'),
    path('add-to-cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<str:pk>/', views.delete_from_cart, name='delete_from_cart'),
    path('increase-quantity/<str:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<str:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('order-checkout/', views.order_checkout, name='order_checkout',)
]