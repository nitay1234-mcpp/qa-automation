import pytest
import logging
from unittest.mock import patch
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
    @patch.object(PaymentProcessor, 'process_payment')
    def test_various_payment_methods(self, mock_process_payment, amount, payment_method, expected_status):
        logger.info(f"Testing payment method: {payment_method} for amount: {amount}")
        mock_process_payment.return_value = {'status': expected_status}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=payment_method)
        logger.debug(f"Response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {payment_method}. Got {response['status']}"

class TestTimeoutScenarios:

    @patch.object(PaymentProcessor, 'process_payment')
    def test_payment_timeout(self, mock_process_payment):
        logger.info("Testing payment processing timeout scenario.")
        mock_process_payment.return_value = {'status': 'timeout'}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'simulate_timeout': True})
        logger.debug(f"Timeout response: {response}")
        assert response['status'] == 'timeout', "Expected 'timeout' status for simulated timeout"

class TestUserNotifications:

    @patch.object(PaymentProcessor, 'send_notification')
    def test_success_notification(self, mock_send_notification):
        logger.info("Testing user success notification.")
        mock_send_notification.return_value = {'message': 'Payment successful.'}
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_success', 'data': {'amount': 100}})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment successful.', "Expected success notification message"

    @patch.object(PaymentProcessor, 'send_notification')
    def test_failure_notification(self, mock_send_notification):
        logger.info("Testing user failure notification.")
        mock_send_notification.return_value = {'message': 'Payment failed: Insufficient funds.'}
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_failure', 'data': {'reason': 'Insufficient funds'}})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment failed: Insufficient funds.', "Expected failure notification message"

    @patch.object(PaymentProcessor, 'send_notification')
    def test_cancellation_notification(self, mock_send_notification):
        logger.info("Testing user cancellation notification.")
        mock_send_notification.return_value = {'message': 'Payment was cancelled.'}
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_cancellation'})
        logger.debug(f"Notification: {notification}")
        assert notification['message'] == 'Payment was cancelled.', "Expected cancellation notification message"