import pytest
import threading
import time
from payment_gateway import PaymentProcessor

class TestPaymentConcurrency:
    def test_simultaneous_payments(self):
        processor = PaymentProcessor()
        results = []

        def make_payment(amount, card_info):
            response = processor.process_payment(amount=amount, card_info=card_info)
            results.append(response['status'])

        card_info = {'number': '4111111111111111', 'cvv': '123'}
        threads = []
        for _ in range(10):  # Simulate 10 simultaneous payments
            t = threading.Thread(target=make_payment, args=(100, card_info))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert results.count('success') == 10, f"Expected 10 successful payments, got {results}"

class TestPaymentRetryLogic:
    def test_retry_failed_payment(self):
        processor = PaymentProcessor()
        card_info = {'number': '4111111111111111', 'cvv': '123', 'simulate_failure': True}
        max_retries = 3
        attempt = 0
        status = 'error'

        while attempt < max_retries and status != 'success':
            response = processor.process_payment(amount=100, card_info=card_info)
            status = response['status']
            attempt += 1

        assert status == 'success', f"Payment was not successful after {max_retries} retries"

class TestWebhookSecurity:
    def test_webhook_with_invalid_signature(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'invalid_signature'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error', "Expected error status for webhook with invalid signature"

    def test_webhook_with_missing_signature(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}  # No signature
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error', "Expected error status for webhook with missing signature"

    def test_webhook_with_valid_signature(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'valid_signature'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed', "Expected processed status for webhook with valid signature"  
