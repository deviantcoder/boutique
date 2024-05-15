from django.db import models
from uuid import uuid4
from users.models import Profile
from django.db.models import Avg


class Product(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(default='default.jpg', null=True, blank=True)

    sku_number = models.IntegerField(default=0, null=True, blank=True)

    is_new = models.BooleanField(default=False, null=True)
    is_sale = models.BooleanField(default=False, null=True)
    is_sold = models.BooleanField(default=False, null=True)

    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    votes_total = models.IntegerField(default=0, null=True, blank=True)

    tags = models.ManyToManyField('Tag', blank=True)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True, blank=True)

    collection = models.ForeignKey('Collection', on_delete=models.SET_NULL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    @property
    def main_image(self):
        main_image = self.productimage_set.filter(is_main=True)
        if main_image.exists():
            return main_image.first().image
        elif self.productimage_set.all():
            return self.productimage_set.all().first().image
        else:
            return self.image

    def get_vote_count(self):
        votes_values = self.review_set.all().values_list('value', flat=True)
        max_vote_count = votes_values.count() * 5

        if votes_values.count() != 0:
            ratio = round((sum(votes_values) / max_vote_count) * 100)
        else:
            ratio = 0

        self.votes_ratio = ratio
        self.votes_total = votes_values.count()

        self.save()

        return ratio

    @property
    def rating_range(self):
        ratio = Product.get_vote_count(self)
        rating_nums = {
            '0': [0, 0],
            '1': [0, 21],
            '2': [21, 41],
            '3': [41, 61],
            '4': [61, 81],
            '5': [81, 101],
        }

        if ratio == 0:
            return range(int(next(iter(rating_nums))))

        for key, value in rating_nums.items():
            if ratio in range(value[0], value[1]):
                return range(int(key))

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('user__id', flat=True)
        return queryset
    
    def is_in_cart(self, user):
        order = user.profile.order_set.all().filter(is_ordered=False)
        if order.exists():
            return order[0].items.filter(product=self).exists()

        # return user.profile.order_set.first().items.filter(product=self).exists()
    
    def is_in_fav(self, user):
        return user.profile.favoriteproducts_set.first().items.filter(product=self).exists()

    class Meta:
        ordering = ['-votes_ratio', '-votes_total', 'created']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True)

    def __str__(self):
        if self.product:
            return f'{self.product.title} -> {self.image.name}'
        return self.image.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(default='default.jpg', upload_to='category_images', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def  __str__(self):
        return f'{self.name} <- {self.category.name}'


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    VOTE_TYPE = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    value = models.IntegerField(default=0, choices=VOTE_TYPE)
    body = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['product__title']

    @property
    def vote_range(self):
        if self.value:
            return range(self.value)
        return 0

    def __str__(self):
        return f'{self.product.title} -> {self.value}'


class Collection(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='collection_images', default='default_collection.jpg', null=True, blank=True)
    body = models.CharField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
