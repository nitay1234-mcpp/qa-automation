import unittest
from payment_processor import PaymentProcessor

class TestUserExperience(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessor()

    def test_successful_transaction_confirmation(self):
        transaction_id = self.processor.process_payment(100)
        confirmation = self.processor.get_confirmation(transaction_id)
        self.assertEqual(confirmation['message'], 'Payment successful!')

    def test_ui_after_successful_payment(self):
        transaction_id = self.processor.process_payment(100)
        ui_state = self.processor.get_ui_state(transaction_id)
        self.assertTrue(ui_state['transaction_success'])
        self.assertEqual(ui_state['transaction_id'], transaction_id)

if __name__ == '__main__':
    unittest.main()