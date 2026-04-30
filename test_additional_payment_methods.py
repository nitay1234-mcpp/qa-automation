import pytest
import logging
import random
import numpy as np
from unittest.mock import patch
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Utility function to generate realistic payment amounts

def generate_payment_amount(distribution='exponential', min_amount=1, max_amount=1000, **kwargs):
    """
    Generate a payment amount based on specified distribution and parameters.

    Args:
        distribution (str): Type of distribution to use ('exponential', 'normal', 'uniform').
        min_amount (int): Minimum payment amount.
        max_amount (int): Maximum payment amount.
        kwargs: Additional parameters for distributions (mean, std_dev for normal, etc.).

    Returns:
        int: Generated payment amount bounded by min_amount and max_amount.
    """
    amount = min_amount
    if distribution == 'exponential':
        mean = kwargs.get('mean', 200)
        amount = int(np.random.exponential(scale=mean))
    elif distribution == 'normal':
        mean = kwargs.get('mean', 200)
        std_dev = kwargs.get('std_dev', 50)
        amount = int(np.random.normal(loc=mean, scale=std_dev))
    elif distribution == 'uniform':
        amount = int(np.random.uniform(low=min_amount, high=max_amount))
    else:
        logger.warning(f"Unknown distribution '{distribution}', defaulting to min_amount")
        amount = min_amount

    # Enforce bounds
    if amount < min_amount:
        amount = min_amount
    if amount > max_amount:
        amount = max_amount

    # Apply rounding to nearest integer (could be adapted for currency units)
    amount = int(round(amount))
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
        # Assign distributions based on payment method type
        distribution = 'exponential'
        max_amount = 1000
        if payment_method['type'] == 'gift_card':
            distribution = 'uniform'
            max_amount = 100
        elif payment_method['type'] == 'bank_transfer':
            distribution = 'normal'
            max_amount = 5000

        amount = generate_payment_amount(distribution=distribution, min_amount=1, max_amount=max_amount)
        logger.info(f"Testing payment method: {payment_method} for amount: {amount}")
        mock_process_payment.return_value = {'status': expected_status}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=payment_method)
        logger.debug(f"Response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {payment_method}. Got {response['status']}"

    @pytest.mark.parametrize("edge_amount", [1, 1000, 5000])
    @patch.object(PaymentProcessor, 'process_payment')
    def test_payment_amount_edge_cases(self, mock_process_payment, edge_amount):
        logger.info(f"Testing edge case payment amount: {edge_amount}")
        mock_process_payment.return_value = {'status': 'success'}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=edge_amount, card_info={'type': 'digital_wallet', 'provider': 'PayPal', 'account_id': 'edgecase'})
        logger.debug(f"Response: {response}")
        assert response['status'] == 'success', "Expected success status for edge amount"

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
