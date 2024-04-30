from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Review


@receiver(post_save, sender=Product)
def set_new(sender, instance, created, **kwargs):
    if created:
        product = instance
        product.is_new = True
        product.save()


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_vote_count(sender, instance, **kwargs):
    product = instance.product
    product.get_vote_count()
    product.save()
