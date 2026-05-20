import unittest

class TestCurrencyConversion(unittest.TestCase):

    def setUp(self):
        # Setup can include initializing conversion rates or mock service
        self.conversion_rates = {
            ('USD', 'EUR'): 0.85,
            ('EUR', 'USD'): 1.18,
            ('USD', 'JPY'): 110.0,
            ('JPY', 'USD'): 0.0091,
        }

    def convert_currency(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        rate = self.conversion_rates.get((from_currency, to_currency))
        if rate is None:
            raise ValueError('Conversion rate not found')
        return amount * rate

    def test_conversion_usd_to_eur(self):
        result = self.convert_currency(100, 'USD', 'EUR')
        self.assertAlmostEqual(result, 85.0, places=2)

    def test_conversion_eur_to_usd(self):
        result = self.convert_currency(100, 'EUR', 'USD')
        self.assertAlmostEqual(result, 118.0, places=2)

    def test_conversion_usd_to_jpy(self):
        result = self.convert_currency(50, 'USD', 'JPY')
        self.assertAlmostEqual(result, 5500.0, places=2)

    def test_conversion_jpy_to_usd(self):
        result = self.convert_currency(1100, 'JPY', 'USD')
        self.assertAlmostEqual(result, 10.01, places=2)

    def test_conversion_same_currency(self):
        result = self.convert_currency(100, 'USD', 'USD')
        self.assertEqual(result, 100)

    def test_conversion_rate_not_found(self):
        with self.assertRaises(ValueError):
            self.convert_currency(100, 'USD', 'INR')

if __name__ == '__main__':
    unittest.main()
