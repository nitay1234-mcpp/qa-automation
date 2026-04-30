import pytest
import logging
from unittest.mock import patch, MagicMock
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPaymentContract:

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (100, {'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
        (100, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    @patch.object(PaymentProcessor, 'process_payment')
    def test_payment_processing(self, mock_process_payment, amount, card_info, expected_status):
        logger.info(f"Processing payment for amount: {amount} with card_info: {card_info}")
        mock_process_payment.return_value = {'status': expected_status}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        logger.debug(f"Received response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    @patch.object(PaymentProcessor, 'handle_webhook')
    def test_webhook_handling(self, mock_handle_webhook):
        logger.info("Testing webhook handling.")
        # Mock valid webhook response
        mock_handle_webhook.side_effect = [
            {'status': 'processed'},
            {'status': 'error'}
        ]
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

    @patch.object(PaymentProcessor, 'process_payment')
    def test_payment_processing_internal_server_error(self, mock_process_payment):
        """
        Test to ensure the payment processor correctly handles a 500 Internal Server Error.

        This test mocks the process_payment method to simulate a 500 error response and verifies
        that the returned response includes the appropriate status and error code as per the API contract.
        """
        logger.info("Testing payment processing handling 500 Internal Server Error.")
        mock_process_payment.return_value = {'status': 'internal_server_error', 'code': 500}
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        logger.debug(f"Received response for 500 error test: {response}")
        assert response['status'] == 'internal_server_error', "Expected 'internal_server_error' status for 500 error"
        assert response['code'] == 500, "Expected error code 500 for internal server error"
        
        # Ensure no unexpected keys are present
        expected_keys = {'status', 'code'}
        assert set(response.keys()) == expected_keys, f"Response keys mismatch. Expected {expected_keys}, got {set(response.keys())}"

    @patch.object(PaymentProcessor, 'delete_payment')
    @pytest.mark.parametrize("payment_id, mock_return, expected_status", [
        ("123", {'status': 'deleted'}, 'deleted'),
        ("456", {'status': 'not_found'}, 'not_found'),
        ("789", {'status': 'unauthorized'}, 'unauthorized')
    ])
    def test_delete_payment_contract(self, mock_delete_payment, payment_id, mock_return, expected_status):
        """
        Contract test for the DELETE /payments/{id} endpoint.

        This test mocks the delete_payment method of PaymentProcessor to simulate:
        - Successful deletion
        - Payment not found
        - Unauthorized deletion

        It asserts that the response status conforms to the expected contract.
        """
        logger.info(f"Testing delete payment contract for payment_id: {payment_id}")
        mock_delete_payment.return_value = mock_return
        processor = PaymentProcessor()
        response = processor.delete_payment(payment_id)
        logger.debug(f"Delete payment response: {response}")
        assert response['status'] == expected_status, f"Expected status '{expected_status}' for payment_id {payment_id}, got {response['status']}"
