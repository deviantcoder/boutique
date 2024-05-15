from django.forms import ModelForm
from django import forms
from .models import Product, ProductImage, Review
from django.forms.models import inlineformset_factory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'quantity',
                  'sku_number', 'is_new', 'is_sale', 'is_sold', 'tags',
                  'category', 'subcategory'
                  ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            # 'subcategory': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('tags'):
                field.widget.attrs.update({'class': ''})
            else:
                field.widget.attrs.update({'class': 'form-control'})


ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image',), extra=3)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Rate a product',
            'body': 'Leave a Review'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
