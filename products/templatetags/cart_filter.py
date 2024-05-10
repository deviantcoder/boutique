from django import template

register = template.Library()

@register.filter
def is_in_cart(product, user):
    return product.is_in_cart(user)


@register.filter
def is_in_fav(product, user):
    return product.is_in_fav(user)
