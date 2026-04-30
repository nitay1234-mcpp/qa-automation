import pytest
import threading
import time
from payment_gateway import PaymentProcessor

class TestPaymentProcessingFlakyDetection:

    def test_concurrent_payment_requests(self):
        processor = PaymentProcessor()
        results = []
        
        def make_payment():
            response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
            results.append(response['status'])

        threads = [threading.Thread(target=make_payment) for _ in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Expect all requests to succeed without race conditions
        assert all(status == 'success' for status in results), f"Concurrent payment failures detected: {results}"

    def test_webhook_retry_mechanism_stress(self):
        processor = PaymentProcessor()
        
        # Simulate rapid webhook retry events
        statuses = []
        for _ in range(30):
            webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}
            response = processor.handle_webhook(webhook_data)
            statuses.append(response['status'])
            time.sleep(0.05)  # slight delay to simulate real retry timing

        # Ensure all webhook retries are processed successfully
        assert all(status == 'processed' for status in statuses), f"Webhook retry failures detected: {statuses}"

    def test_webhook_retry_invalid_event_handling(self):
        processor = PaymentProcessor()
        
        # Test rapid firing of invalid webhook events
        statuses = []
        for _ in range(10):
            webhook_data = {'event': 'invalid_event'}
            response = processor.handle_webhook(webhook_data)
            statuses.append(response['status'])

        # All invalid events should return 'error'
        assert all(status == 'error' for status in statuses), f"Invalid webhook event handling errors: {statuses}"

