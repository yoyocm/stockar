import unittest
from unittest import TestCase

from stockar.billing_service_in_memory import BillingServiceInMemory
from stockar.models import StorageOffer


class StorageOfferTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.billing_service = BillingServiceInMemory()

    def setUp(self):
        StorageOffer.objects.all().delete()

    def test_should_create_product_on_billing_service_when_storage_offer_has_been_created(self):
        storage_offer = StorageOffer(
            name='standard offer',
            description='standard offer description',
            monthly_price=1.0
        )

        storage_offer.save()

        retrieved_billing_product = self.billing_service.get_product(storage_offer.id)
        self.assertEqual(retrieved_billing_product.id, storage_offer.id)
        self.assertEqual(retrieved_billing_product.monthly_price, storage_offer.monthly_price)


if __name__ == '__main__':
    unittest.main()
