from django.contrib import admin
from . import models


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    extra = 1


class SubcategoryInline(admin.StackedInline):
    model = models.Subcategory


# class ProductInline(admin.TabularInline):
#     model = models.Product


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    class Meta:
        model = models.Product


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]

    class Meta:
        model = models.Category


@admin.register(models.Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Collection)
admin.site.register(models.Tag)
admin.site.register(models.Review)
