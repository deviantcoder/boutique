from django.db import models
from products.models import Product
from uuid import uuid4
from users.models import Profile


class FavItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['product']

    def __str__(self):
        return self.product.title


class FavoriteProducts(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(FavItem)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def get_items(self):
        return self.items.all()
    
    class Meta:
        ordering = ['-owner']

    def __str__(self) -> str:
        return f'{self.owner.username}: fav products'
