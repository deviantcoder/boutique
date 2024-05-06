from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Order


@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    try:
        for item in instance.items.all():
            item.delete()
    except Order.DoesNotExist:
        pass