import os

from django.apps import AppConfig

from stockar.billing_service_impl import BillingServiceImpl
from stockar.billing_service_in_memory import BillingServiceInMemory


class StockarConfig(AppConfig):
    name = 'stockar'

    def ready(self):
        from . import signals
