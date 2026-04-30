import unittest

# Mock payment processing function
# Replace this with actual payment API call in real implementation

def process_payment(amount, currency, card_details, base_currency=None):
    supported_currencies = ['USD', 'EUR']
    if currency.upper() not in supported_currencies:
        return {'success': False, 'error': 'Unsupported currency'}
    if amount <= 0:
        return {'success': False, 'error': 'Invalid amount'}
    # Simulate currency conversion check
    conversion_rate_applied = False
    if base_currency and base_currency != currency:
        conversion_rate_applied = True
    # Simulate success response
    return {'success': True, 'currency': currency.upper(), 'conversion_rate_applied': conversion_rate_applied}


class TestCurrencyHandling(unittest.TestCase):

    def setUp(self):
        self.valid_card = {'number': '4111111111111111', 'cvv': '123', 'expiry': '12/25'}

    def test_supported_currency_usd(self):
        response = process_payment(100, 'USD', self.valid_card)
        self.assertTrue(response['success'])
        self.assertEqual(response['currency'], 'USD')

    def test_supported_currency_eur(self):
        response = process_payment(100, 'EUR', self.valid_card)
        self.assertTrue(response['success'])
        self.assertEqual(response['currency'], 'EUR')
        self.assertFalse(response['conversion_rate_applied'])  # No conversion if base currency not specified

    def test_unsupported_currency(self):
        response = process_payment(100, 'XYZ', self.valid_card)
        self.assertFalse(response['success'])
        self.assertEqual(response['error'], 'Unsupported currency')

    def test_currency_conversion(self):
        response = process_payment(100, 'EUR', self.valid_card, base_currency='USD')
        self.assertTrue(response['success'])
        self.assertEqual(response['currency'], 'EUR')
        self.assertTrue(response['conversion_rate_applied'])

    def test_zero_negative_amount(self):
        response_zero = process_payment(0, 'USD', self.valid_card)
        response_negative = process_payment(-100, 'USD', self.valid_card)
        self.assertFalse(response_zero['success'])
        self.assertEqual(response_zero['error'], 'Invalid amount')
        self.assertFalse(response_negative['success'])
        self.assertEqual(response_negative['error'], 'Invalid amount')

    def test_currency_code_format_validation(self):
        # Lowercase currency code should be normalized or rejected
        response = process_payment(100, 'usd', self.valid_card)
        self.assertTrue(response['success'])
        self.assertEqual(response['currency'], 'USD')


if __name__ == '__main__':
    unittest.main()
