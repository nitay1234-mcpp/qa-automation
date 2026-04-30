import pytest
from payment_gateway import PaymentProcessor

class TestSecurityEnhancements:

    def test_authentication_required(self):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, auth_token=None)
        assert response['status'] == 'unauthorized', "Expected 'unauthorized' status for missing auth token"

    def test_authorization_required(self):
        processor = PaymentProcessor()
        response = processor.cancel_payment(payment_id='test-payment-id', auth_token='invalid_token')
        assert response['status'] == 'forbidden', "Expected 'forbidden' status for invalid auth token"

    def test_sql_injection_attempt(self):
        processor = PaymentProcessor()
        malicious_input = "'; DROP TABLE payments; --"
        response = processor.process_payment(amount=100, card_info={'number': malicious_input, 'cvv': '123'})
        assert response['status'] != 'success', "SQL injection attempt should not succeed"

    def test_xss_attack_attempt(self):
        processor = PaymentProcessor()
        malicious_input = "<script>alert('XSS')</script>"
        response = processor.process_payment(amount=100, card_info={'number': malicious_input, 'cvv': '123'})
        assert response['status'] != 'success', "XSS attack attempt should not succeed"

    def test_csrf_protection(self):
        processor = PaymentProcessor()
        # Assuming csrf_token is required and validated
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, csrf_token=None)
        assert response['status'] == 'forbidden', "Expected 'forbidden' status for missing CSRF token"