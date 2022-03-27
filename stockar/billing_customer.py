class BillingCustomer:
    def __init__(self, email, name, stripe_customer_id):
        self.email = email
        self.name = name
        self.stripe_customer_id = stripe_customer_id
