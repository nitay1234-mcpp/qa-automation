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

    def test_race_condition(self):
        processor = PaymentProcessor()
        results = []

        def make_payment():
            response = processor.process_payment(amount=50, card_info={'number': '4111111111111111', 'cvv': '123'})
            results.append(response['status'])

        threads = [threading.Thread(target=make_payment) for _ in range(20)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert results.count('success') == 20, f"Expected 20 successful payments, got {results}"

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

    def test_retry_with_backoff(self):
        processor = PaymentProcessor()
        card_info = {'number': '4111111111111111', 'cvv': '123', 'simulate_failure': True}
        max_retries = 3
        delay = 1
        attempt = 0
        status = 'error'

        while attempt < max_retries and status != 'success':
            response = processor.process_payment(amount=100, card_info=card_info)
            status = response['status']
            if status != 'success':
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            attempt += 1

        assert status == 'success', "Expected success after retries with backoff"

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

    def test_webhook_with_delayed_event(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'valid_signature', 'delayed': True}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed', "Expected processed status for delayed webhook event"

    def test_webhook_with_duplicate_event(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'valid_signature', 'duplicate': True}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed', "Expected processed status for duplicate webhook event"