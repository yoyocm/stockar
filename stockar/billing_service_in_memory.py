from stockar.billing_service import BillingService
from stockar.billing_service_error import BillingServiceError
from stockar.singleton import SingletonMetaclass


class BillingServiceInMemory(BillingService, metaclass=SingletonMetaclass):
    def __init__(self):
        super().__init__()
        self.products = {}

    def get_product(self, id):
        return self.products.get(id, BillingServiceError.PRODUCT_NOT_FOUND)

    def create_product(self, billing_product):
        self.products[billing_product.id] = billing_product
