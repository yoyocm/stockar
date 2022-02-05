import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from stockar.billing_product import BillingProduct
from stockar.billing_service_impl import BillingServiceImpl
from stockar.billing_service_in_memory import BillingServiceInMemory
from stockar.models import StorageOffer


@receiver(post_save, sender=StorageOffer)
def create_billing_product(sender, instance, created, **kwargs):
    billing_service = BillingServiceInMemory() if os.getenv('ENV') else BillingServiceImpl()

    if created:
        billing_product = BillingProduct(id=instance.id, name=instance.name, description=instance.description, monthly_price=instance.monthly_price)
        billing_service.create_product(billing_product)
