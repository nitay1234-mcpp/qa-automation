import pytest
from payment_gateway import PaymentProcessor

class TestPaymentProcessing:

    def test_fraud_detection(self):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert response['status'] == 'success'
        
        # Simulate a fraudulent transaction
        response = processor.process_payment(amount=100, card_info={'number': '1234567890123456', 'cvv': '123'})
        assert response['status'] == 'fraud_detected'

    def test_webhook_handling(self):
        processor = PaymentProcessor()
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}  
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'processed'
        
        # Simulate an invalid webhook
        webhook_data = {'event': 'invalid_event'}
        response = processor.handle_webhook(webhook_data)
        assert response['status'] == 'error'

    def test_edge_cases_payment_methods(self):
        processor = PaymentProcessor()
        # Test with an expired card
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'})
        assert response['status'] == 'error'
        
        # Test with a payment method not accepted
        response = processor.process_payment(amount=100, card_info={'number': '5500000000000004', 'cvv': '123'})
        assert response['status'] == 'payment_method_not_accepted'