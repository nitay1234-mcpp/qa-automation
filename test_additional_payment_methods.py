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
        (75, {'type': 'bank_transfer', 'account_number': '', 'routing_number': '987654321'}, 'error')
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

class TestUserNotifications:

    def test_success_notification(self):
        logger.info("Testing user success notification.")
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_success', 'data': {'amount': 100}})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment successful.', "Expected success notification message"

    def test_failure_notification(self):
        logger.info("Testing user failure notification.")
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_failure', 'data': {'reason': 'Insufficient funds'}})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment failed: Insufficient funds.', "Expected failure notification message"

    def test_cancellation_notification(self):
        logger.info("Testing user cancellation notification.")
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_cancellation'})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment was cancelled.', "Expected cancellation notification message"
