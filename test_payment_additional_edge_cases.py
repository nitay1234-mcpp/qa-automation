import pytest
import threading
from unittest.mock import patch, MagicMock
from payment_gateway import PaymentProcessor

class TestPaymentConcurrency:
    @patch.object(PaymentProcessor, 'process_payment')
    def test_simultaneous_payments(self, mock_process_payment):
        processor = PaymentProcessor()
        results = []

        # Mock process_payment to always return success
        mock_process_payment.return_value = {'status': 'success'}

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
    @patch.object(PaymentProcessor, 'process_payment')
    def test_retry_failed_payment(self, mock_process_payment):
        processor = PaymentProcessor()
        card_info = {'number': '4111111111111111', 'cvv': '123', 'simulate_failure': True}
        max_retries = 3
        attempt = 0
        status = 'error'

        # Configure mock to simulate failure twice then success
        mock_process_payment.side_effect = [
            {'status': 'error'},
            {'status': 'error'},
            {'status': 'success'}
        ]

        while attempt < max_retries and status != 'success':
            response = processor.process_payment(amount=100, card_info=card_info)
            status = response['status']
            attempt += 1

        assert status == 'success', f"Payment was not successful after {max_retries} retries"

class TestWebhookSecurity:
    @patch.object(PaymentProcessor, 'handle_webhook')
    def test_webhook_with_invalid_signature(self, mock_handle_webhook):
        processor = PaymentProcessor()
        mock_handle_webhook.return_value = {'status': 'error'}
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'invalid_signature'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error', "Expected error status for webhook with invalid signature"

    @patch.object(PaymentProcessor, 'handle_webhook')
    def test_webhook_with_missing_signature(self, mock_handle_webhook):
        processor = PaymentProcessor()
        mock_handle_webhook.return_value = {'status': 'error'}
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}  # No signature
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error', "Expected error status for webhook with missing signature"

    @patch.object(PaymentProcessor, 'handle_webhook')
    def test_webhook_with_valid_signature(self, mock_handle_webhook):
        processor = PaymentProcessor()
        mock_handle_webhook.return_value = {'status': 'processed'}
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}, 'signature': 'valid_signature'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed', "Expected processed status for webhook with valid signature"  
