from locust import HttpUser, task, between
import random

class WebhookLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def send_webhook_notification(self):
        # Simulate webhook notification with retries
        self.client.post("/webhook/notify", json={"retry_count": random.randint(1, 5)})

class PaymentFlowLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def valid_payment(self):
        payload = {
            "payment_method": random.choice(["paypal", "credit_card", "third_party_gateway"]),
            "amount": random.uniform(1.0, 500.0),
            "card_expired": False,
            "fraudulent": False
        }
        self.client.post("/payment/process", json=payload)

    @task(1)
    def fraudulent_payment(self):
        payload = {
            "payment_method": random.choice(["paypal", "credit_card", "third_party_gateway"]),
            "amount": random.uniform(1.0, 500.0),
            "card_expired": False,
            "fraudulent": True
        }
        self.client.post("/payment/process", json=payload)

    @task(1)
    def expired_card_payment(self):
        payload = {
            "payment_method": random.choice(["paypal", "credit_card", "third_party_gateway"]),
            "amount": random.uniform(1.0, 500.0),
            "card_expired": True,
            "fraudulent": False
        }
        self.client.post("/payment/process", json=payload)

    @task(1)
    def unsupported_method_payment(self):
        payload = {
            "payment_method": "unsupported_method",
            "amount": random.uniform(1.0, 500.0),
            "card_expired": False,
            "fraudulent": False
        }
        self.client.post("/payment/process", json=payload)

class RefundLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def full_refund(self):
        payload = {"refund_amount": random.uniform(1.0, 200.0), "partial": False}
        self.client.post("/refund/process", json=payload)

    @task(2)
    def partial_refund_valid(self):
        payload = {"refund_amount": random.uniform(1.0, 100.0), "partial": True}
        self.client.post("/refund/process", json=payload)

    @task(1)
    def refund_invalid_amount(self):
        invalid_amounts = [0, -1, -100, random.uniform(-500, 0)]
        payload = {"refund_amount": random.choice(invalid_amounts), "partial": True}
        self.client.post("/refund/process", json=payload)

class EdgeCaseLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def zero_amount_payment(self):
        payload = {"payment_method": "credit_card", "amount": 0, "card_expired": False, "fraudulent": False}
        self.client.post("/payment/process", json=payload)

    @task(2)
    def high_amount_payment(self):
        payload = {"payment_method": "credit_card", "amount": 1000000, "card_expired": False, "fraudulent": False}
        self.client.post("/payment/process", json=payload)

    @task(2)
    def invalid_card_format(self):
        payload = {"payment_method": "credit_card", "amount": 50, "card_expired": False, "fraudulent": False, "card_number": "1234abcd5678"}
        self.client.post("/payment/process", json=payload)

class OnboardingLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def new_merchant_onboarding(self):
        payload = {
            "merchant_name": "Test Merchant",
            "secure_data": "encrypted_data",
            "real_time_processing": True
        }
        self.client.post("/merchant/onboard", json=payload)
