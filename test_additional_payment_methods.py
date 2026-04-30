import pytest
import logging
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestAdditionalPaymentMethods:

    @pytest.mark.parametrize("amount, payment_method, expected_status", [
        (100, {'type': 'digital_wallet', 'provider': 'PayPal', 'account_id': 'user123'}, 'success'),
        (200, {'type': 'digital_wallet', 'provider': 'Apple Pay', 'account_id': 'user456'}, 'success'),
        (50, {'type': 'gift_card', 'card_number': 'GIFT123456789', 'pin': '1234'}, 'success'),
        (75, {'type': 'bank_transfer', 'account_number': '123456789', 'routing_number': '987654321'}, 'success'),
        (100, {'type': 'digital_wallet', 'provider': 'UnknownWallet', 'account_id': 'user999'}, 'payment_method_not_accepted'),
        (50, {'type': 'gift_card', 'card_number': 'INVALIDCARD', 'pin': '0000'}, 'error'),
        (75, {'type': 'bank_transfer', 'account_number': '', 'routing_number': '987654321'}, 'error'),
        # Additional edge cases
        (0, {'type': 'digital_wallet', 'provider': 'PayPal', 'account_id': 'user000'}, 'error'),  # Zero amount
        (10000, {'type': 'gift_card', 'card_number': 'GIFT999999999', 'pin': '9999'}, 'success'),  # Large amount
        (100, {'type': 'digital_wallet', 'provider': 'Google Pay', 'account_id': 'user789'}, 'success')  # New provider
    ])
    def test_various_payment_methods(self, amount, payment_method, expected_status):
        logger.info(f"Testing payment method: {payment_method} for amount: {amount}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=payment_method)
        logger.debug(f"Response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {payment_method}. Got {response['status']}"

class TestTimeoutScenarios:

    def test_payment_timeout(self):
        logger.info("Testing payment processing timeout scenario.")
        processor = PaymentProcessor()
        # Simulate timeout by passing a special flag or mock if supported
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'simulate_timeout': True})
        logger.debug(f"Timeout response: {response}")
        assert response['status'] == 'timeout', "Expected 'timeout' status for simulated timeout"

    def test_timeout_with_retry(self):
        logger.info("Testing payment timeout with retry logic.")
        processor = PaymentProcessor()
        max_retries = 3
        attempt = 0
        status = 'timeout'

        while attempt < max_retries and status == 'timeout':
            response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'simulate_timeout': True})
            status = response['status']
            attempt += 1
            logger.debug(f"Attempt {attempt} status: {status}")

        assert status != 'timeout', "Expected eventual success after retrying timeout"

class TestUserNotifications:

    @pytest.mark.parametrize("event, expected_message", [
        ('payment_success', 'Payment successful.'),
        ('payment_failure', 'Payment failed: Insufficient funds.'),
        ('payment_cancellation', 'Payment was cancelled.'),
        # Additional notification types
        ('payment_pending', 'Payment is pending.'),
        ('refund_processed', 'Refund processed successfully.'),
        ('chargeback_initiated', 'Chargeback has been initiated.')
    ])
    def test_notifications(self, event, expected_message):
        logger.info(f"Testing user notification for event: {event}")
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': event})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == expected_message, f"Expected message '{expected_message}' for event '{event}'"

    def test_notification_with_additional_data(self):
        logger.info("Testing notification with additional data.")
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_success', 'data': {'amount': 100, 'currency': 'USD'}})
        logger.debug(f"Notification: {notification}")
        assert 'Payment successful' in notification['message'], "Expected success message in notification with data"
