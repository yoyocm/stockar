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
        retrieved_price = stripe.Price.list(product=id).data[0]

        return BillingProduct(
            id=retrieved_product.id,
            name=retrieved_product.name,
            description=retrieved_product.description,
            monthly_price=retrieved_price.unit_amount / 100
        )

    def create_product(self, billing_product):
        product = stripe.Product.create(
            id=billing_product.id,
            name=billing_product.name,
            description=billing_product.description
        )
        stripe.Price.create(
            product=product.id,
            currency='eur',
            unit_amount=billing_product.monthly_price * 100,
            recurring={
                'interval': 'month'
            }
        )

    def clear(self):
        for product in stripe.Product.list(active=True):
            stripe.Product.modify(product.id, active=False)
