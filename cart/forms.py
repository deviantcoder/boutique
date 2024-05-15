from django.forms import ModelForm
from django import forms
from .models import OrderCheckout


class CheckoutForm(ModelForm):
    class Meta:
        model = OrderCheckout
        fields = ['first_name', 'last_name', 'email', 
                  'country', 'city', 'address', 'payment_method',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})