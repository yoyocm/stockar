import uuid

from stockar.billing_customer import BillingCustomer
from stockar.billing_service import BillingService
from stockar.billing_service_error import BillingServiceError
from stockar.singleton import SingletonMetaclass


class BillingServiceInMemory(BillingService, metaclass=SingletonMetaclass):
    def __init__(self):
        super().__init__()
        self.customers = {}
        self.products = {}

    def get_product(self, id):
        return self.products.get(id, BillingServiceError.PRODUCT_NOT_FOUND)

    def create_product(self, billing_product):
        self.products[billing_product.id] = billing_product

    def create_customer(self, account):
        customer = BillingCustomer(account.email, account.first_name + ' ' + account.last_name, uuid.uuid4())
        self.customers[customer.email] = customer
        return customer

    def get_customer(self, email):
        return self.customers.get(email, BillingServiceError.CUSTOMER_NOT_FOUND)
