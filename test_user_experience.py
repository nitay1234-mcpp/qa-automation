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

    def test_ui_after_failed_payment(self):
        transaction_id = self.processor.process_payment(0)  # Simulate failed payment with 0 amount
        ui_state = self.processor.get_ui_state(transaction_id)
        self.assertFalse(ui_state['transaction_success'])
        self.assertEqual(ui_state['transaction_id'], transaction_id)
        self.assertEqual(ui_state.get('error_message'), 'Invalid payment amount')

    def test_ui_during_pending_payment(self):
        transaction_id = self.processor.process_payment(100, simulate_pending=True)  # Simulate pending state
        ui_state = self.processor.get_ui_state(transaction_id)
        self.assertEqual(ui_state['transaction_status'], 'pending')
        self.assertEqual(ui_state['transaction_id'], transaction_id)

if __name__ == '__main__':
    unittest.main()
