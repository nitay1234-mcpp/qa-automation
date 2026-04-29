import pytest
import logging
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPaymentProcessing:

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (100, {'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
        (100, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_payment_processing(self, amount, card_info, expected_status):
        logger.info(f"Processing payment for amount: {amount} with card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        logger.debug(f"Received response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    def test_webhook_handling(self):
        logger.info("Testing webhook handling.")
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}  
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Webhook response: {response}")
        assert response['status'] == 'processed', "Expected 'processed' status for valid webhook"
        
        # Simulate an invalid webhook
        webhook_data = {'event': 'invalid_event'}
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Invalid webhook response: {response}")
        assert response['status'] == 'error', "Expected 'error' status for invalid webhook"

    def test_edge_cases_payment_methods(self):
        logger.info("Testing edge cases for payment methods.")
        processor = PaymentProcessor()
        # Test with an expired card
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'})
        logger.debug(f"Expired card response: {response}")
        assert response['status'] == 'error', "Expected 'error' status for expired card"
        
        # Test with a payment method not accepted
        response = processor.process_payment(amount=100, card_info={'number': '5500000000000004', 'cvv': '123'})
        logger.debug(f"Not accepted card response: {response}")
        assert response['status'] == 'payment_method_not_accepted', "Expected 'payment_method_not_accepted' status for non-accepted card"
    
    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (200, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_invalid_card_length(self, amount, card_info, expected_status):
        logger.info(f"Testing invalid card length for amount: {amount} and card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        logger.debug(f"Invalid card length response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    @pytest.mark.parametrize("card_info, expected_status", [
        ({'number': '4111A11111111111', 'cvv': '123'}, 'error'),  # Invalid card format
        ({'number': '4111-1111-1111-1111', 'cvv': '123'}, 'error'),  # Non-numeric characters
        ({'number': '1234', 'cvv': '123'}, 'error'),  # Too short
        ({'number': '4111111111111111111111111111111111', 'cvv': '123'}, 'error')  # Too long
    ])
    def test_invalid_card_formats(self, card_info, expected_status):
        logger.info(f"Testing invalid card format with card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info=card_info)
        logger.debug(f"Invalid card format response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    @pytest.mark.parametrize("amount", [0, 1000000])  # Boundary values
    def test_boundary_values_for_amount(self, amount):
        logger.info(f"Testing boundary value payment with amount: {amount}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info={'number': '4111111111111111', 'cvv': '123'})
        logger.debug(f"Boundary value response: {response}")
        if amount == 0:
            assert response['status'] == 'error', "Expected 'error' for zero amount"
        else:
            assert response['status'] == 'success', "Expected 'success' for a valid amount"

    def test_multiple_payment_attempts(self):
        logger.info("Testing multiple rapid payment attempts.")
        processor = PaymentProcessor()
        for _ in range(5):  # Simulating 5 rapid attempts
            response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
            logger.debug(f"Rapid payment response: {response}")
            assert response['status'] == 'success', "Expected 'success' for valid payment attempt"

    @pytest.mark.parametrize("card_info, expected_status", [
        ({'number': '4111111111111111', 'cvv': '123'}, 'fraud_detected'),  # Known fraudulent card
        ({'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected')   # Another known fraud
    ])
    def test_fraud_detection_scenarios(self, card_info, expected_status):
        logger.info(f"Testing fraud detection with card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info=card_info)
        logger.debug(f"Fraud detection response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    @pytest.mark.parametrize("expiry_date, expected_status", [
        ('01/23', 'error'),  # Expired card
        ('12/22', 'error'),  # Recently expired card
        ('09/23', 'success')  # Valid upcoming expiry
    ])
    def test_expiry_dates(self, expiry_date, expected_status):
        logger.info(f"Testing card expiry date: {expiry_date}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'expiry': expiry_date})
        logger.debug(f"Expiry date response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for expiry: {expiry_date}. Got {response['status']}"

    def test_webhook_variations(self):
        logger.info("Testing variations of webhook handling.")
        processor = PaymentProcessor()
        
        # Valid webhook with missing fields
        webhook_data = {'event': 'payment_success'}
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Webhook response with missing fields: {response}")
        assert response['status'] == 'processed', "Expected 'processed' status for valid webhook with missing fields"

        # Extra fields in webhook
        webhook_data = {'event': 'payment_success', 'extra_field': 'extra_value'}
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Webhook response with extra fields: {response}")
        assert response['status'] == 'processed', "Expected 'processed' status for valid webhook with extra fields"

        # Invalid event type
        webhook_data = {'event': 'invalid_event'}
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Invalid webhook response: {response}")
        assert response['status'] == 'error', "Expected 'error' status for invalid webhook"

    @pytest.mark.parametrize("card_info, expected_status", [
        ({'number': '4111-1111-1111-1111', 'cvv': '123'}, 'error'),  # Invalid card format
        ({'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted'),  # Not accepted card
        ({'number': '4111A1111111111', 'cvv': '123'}, 'error')  # Invalid format
    ])
    def test_edge_cases_payment_methods(self, card_info, expected_status):
        logger.info(f"Testing edge cases for payment methods with card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info=card_info)
        logger.debug(f"Edge case response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"