import uuid
from unittest import TestCase

import stripe

from stockar import settings
from stockar.billing_product import BillingProduct
from stockar.billing_service_impl import BillingServiceImpl


class TestBillingServiceImplInt(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.billing_service = BillingServiceImpl()


        cls.billing_service.clear()

    def test_should_persist_product_in_stripe(self):
        product = BillingProduct(id=str(uuid.uuid4()), name='product name', description='product description', monthly_price=1)

        self.billing_service.create_product(product)

        retrieved_product = self.billing_service.get_product(product.id)
        self.assertEqual(retrieved_product.id, product.id)
        self.assertEqual(retrieved_product.name, product.name)
        self.assertEqual(retrieved_product.description, product.description)

    def test_should_persist_price_in_stripe(self):
        product = BillingProduct(id=str(uuid.uuid4()), name='product name', description='product description', monthly_price=1)

        self.billing_service.create_product(product)

        retrieved_product = self.billing_service.get_product(product.id)
        self.assertEqual(retrieved_product.monthly_price, product.monthly_price)
