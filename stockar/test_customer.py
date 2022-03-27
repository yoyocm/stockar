import unittest
from unittest import TestCase

from stockar import models
from stockar.billing_service_error import BillingServiceError
from stockar.billing_service_in_memory import BillingServiceInMemory
from stockar.models import Account


class CustomerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.billing_service = BillingServiceInMemory()

    def setUp(self):
        Account.objects.all().delete()

    def test_should_create_customer_on_billing_service_when_non_admin_account_has_been_created(self):
        account = Account(
            email='email@domain.org',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=False,
            is_admin=False
        )

        account.save()

        retrieved_customer = self.billing_service.get_customer(account.email)
        self.assertEqual(retrieved_customer.email, 'email@domain.org')
        self.assertEqual(retrieved_customer.name, 'John Doe')
        self.assertIsNotNone(retrieved_customer.stripe_customer_id)

    def test_should_not_create_customer_on_billing_service_when_admin_account_has_been_created(self):
        account = Account(
            email='admin@domain.org',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=False,
            is_admin=True
        )

        account.save()

        retrieved_customer = self.billing_service.get_customer(account.email)
        self.assertEqual(retrieved_customer, BillingServiceError.CUSTOMER_NOT_FOUND)

    def test_should_not_create_customer_on_billing_service_when_staff_account_has_been_created(self):
        account = Account(
            email='admin@domain.org',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=True,
            is_admin=False
        )

        account.save()

        retrieved_customer = self.billing_service.get_customer(account.email)
        self.assertEqual(retrieved_customer, BillingServiceError.CUSTOMER_NOT_FOUND)

    def test_should_insert_billing_service_customer_id_in_account_when_non_admin_account_has_been_created(self):
        account = Account(
            email='email@domain.org',
            first_name='John',
            last_name='Doe',
            is_active=True,
            is_staff=False,
            is_admin=False
        )

        account.save()

        retrieved_account = models.Account.objects.get(pk=account.pk)
        self.assertIsNotNone(retrieved_account.stripe_customer_id)


if __name__ == '__main__':
    unittest.main()
