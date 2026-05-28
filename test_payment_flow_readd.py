import pytest
from payment_gateway import PaymentProcessor

class TestPaymentFlowReAdd:

    def setup_method(self):
        self.processor = PaymentProcessor()

    def test_validate_payment_with_paypal(self):
        # Simulate user selecting PayPal payment method and completing payment
        payment_method = 'paypal'
        amount = 100
        response = self.processor.process_payment(amount=amount, payment_method=payment_method)
        assert response['status'] == 'success', "Payment should be processed successfully with PayPal"

    def test_validate_payment_with_discount_code(self):
        # Simulate user applying a valid discount code and completing payment
        discount_code = 'DISCOUNT10'
        amount = 90  # Assuming discount applied
        response = self.processor.process_payment(amount=amount, discount_code=discount_code)
        assert response['status'] == 'success', "Payment should be processed successfully with discount code"

    def test_validate_payment_with_network_timeout(self):
        # Simulate network timeout scenario
        self.processor.simulate_network_timeout(True)
        amount = 100
        response = self.processor.process_payment(amount=amount)
        self.processor.simulate_network_timeout(False)  # Reset simulation
        assert response['status'] == 'error', "Payment should fail due to network timeout"

    def test_validate_user_notification_on_payment_status(self):
        # Simulate a successful payment and check user notification
        amount = 100
        response = self.processor.process_payment(amount=amount)
        notification = self.processor.get_user_notification()
        assert response['status'] == 'success', "Payment should be successful"
        assert 'Payment successful' in notification['message'], "User should receive payment success notification"
