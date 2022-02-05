import stripe

from stockar import settings
from stockar.billing_product import BillingProduct
from stockar.billing_service import BillingService
from stockar.singleton import SingletonMetaclass


class BillingServiceImpl(BillingService, metaclass=SingletonMetaclass):
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def get_product(self, id):
        retrieved_product = stripe.Product.retrieve(id)
        return BillingProduct(
            id=retrieved_product.id,
            name=retrieved_product.name,
            description=retrieved_product.description
        )

    def create_product(self, billing_product):
        stripe.Product.create(
            id=billing_product.id,
            name=billing_product.name,
            description=billing_product.description
        )

    def clear(self):
        for product in stripe.Product.list(active=True):
            stripe.Product.delete(product.id)
