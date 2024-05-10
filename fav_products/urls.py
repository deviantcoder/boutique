from django.urls import path
from . import views

urlpatterns = [
    path('', views.fav_products_details, name='fav_products'),
    path('delete_item/<str:pk>/', views.delete_from_fav, name='delete_from_fav'),
    path('add_to_fav/<str:pk>/', views.add_to_fav, name='add_to_fav'),
]