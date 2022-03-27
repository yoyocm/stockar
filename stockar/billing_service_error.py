from enum import Enum


class BillingServiceError(Enum):
    PRODUCT_NOT_FOUND = 1
    CUSTOMER_NOT_FOUND = 2