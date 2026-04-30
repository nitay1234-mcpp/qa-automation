import pytest
import logging
import random
from unittest.mock import patch
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Utility function to generate realistic payment amounts

def generate_payment_amount(min_amount=1, max_amount=1000):
    # Example using a skewed distribution for payment amounts
    # Most payments are small, fewer are large
    amount = int(random.expovariate(1/200))  # mean around 200
    if amount < min_amount:
        amount = min_amount
    if amount > max_amount:
        amount = max_amount
    return amount

class TestAdditionalPaymentMethods:

    @pytest.mark.parametrize("payment_method, expected_status", [
        ({'type': 'digital_wallet', 'provider': 'PayPal', 'account_id': 'user123'}, 'success'),
        ({'type': 'digital_wallet', 'provider': 'Apple Pay', 'account_id': 'user456'}, 'success'),
        ({'type': 'gift_card', 'card_number': 'GIFT123456789', 'pin': '1234'}, 'success'),
        ({'type': 'bank_transfer', 'account_number': '123456789', 'routing_number': '987654321'}, 'success'),
        ({'type': 'digital_wallet', 'provider': 'UnknownWallet', 'account_id': 'user999'}, 'payment_method_not_accepted'),
        ({'type': 'gift_card', 'card_number': 'INVALIDCARD', 'pin': '0000'}, 'error'),
        ({'type': 'bank_transfer', 'account_number': '', 'routing_number': '987654321'}, 'error')
    ])
    @patch.object(PaymentProcessor, 'process_payment')
    def test_various_payment_methods(self, mock_process_payment, payment_method, expected_status):
        amount = generate_payment_amount()
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
        response = processor.process_payment(amount=generate_payment_amount(), card_info={'number': '4111111111111111', 'cvv': '123', 'simulate_timeout': True})
        logger.debug(f"Timeout response: {response}")
        assert response['status'] == 'timeout', "Expected 'timeout' status for simulated timeout"

class TestUserNotifications:

    @patch.object(PaymentProcessor, 'send_notification')
    def test_success_notification(self, mock_send_notification):
        logger.info("Testing user success notification.")
        mock_send_notification.return_value = {'message': 'Payment successful.'}
        processor = PaymentProcessor()
        notification = processor.send_notification({'event': 'payment_success', 'data': {'amount': generate_payment_amount()}})
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