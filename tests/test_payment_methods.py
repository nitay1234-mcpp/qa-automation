import unittest
from payment_processor import PaymentProcessor

class TestPaymentProcessingMethods(unittest.TestCase):

    def test_payment_processing_credit_card(self):
        response = PaymentProcessor.process_payment(100, method='credit_card')
        self.assertEqual(response.status, 'success')

    def test_payment_processing_debit_card(self):
        response = PaymentProcessor.process_payment(100, method='debit_card')
        self.assertEqual(response.status, 'success')

    def test_payment_processing_alternative_method(self):
        response = PaymentProcessor.process_payment(100, method='paypal')
        self.assertEqual(response.status, 'success')

if __name__ == '__main__':
    unittest.main()