import pytest
from payment_gateway import PaymentProcessor

class TestPaymentProcessing:

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (100, {'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
        (100, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_payment_processing(self, amount, card_info, expected_status):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}"

    def test_webhook_handling(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}  
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed', "Expected 'processed' status for valid webhook"
        
        # Simulate an invalid webhook
        webhook_data = {'event': 'invalid_event'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error', "Expected 'error' status for invalid webhook"

    def test_edge_cases_payment_methods(self):
        processor = PaymentProcessor()
        # Test with an expired card
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'})
        assert response['status'] == 'error', "Expected 'error' status for expired card"
        
        # Test with a payment method not accepted
        response = processor.process_payment(amount=100, card_info={'number': '5500000000000004', 'cvv': '123'})
        assert response['status'] == 'payment_method_not_accepted', "Expected 'payment_method_not_accepted' status for non-accepted card"
    
    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (200, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_invalid_card_length(self, amount, card_info, expected_status):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}"
