import unittest
import requests

BASE_URL = "http://localhost:8000"  # Assuming local test server

class TestUntestedEndpoints(unittest.TestCase):

    def test_post_payments_invalid_card_details(self):
        payload = {
            "card_number": "1234-5678-9012-3456",
            "expiration_date": "01/20",
            "cvv": "123",
            "amount": 100
        }
        response = requests.post(f"{BASE_URL}/payments", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid card details", response.text)

    def test_get_transactions_with_valid_filters(self):
        params = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "page": 1,
            "page_size": 10
        }
        response = requests.get(f"{BASE_URL}/transactions", params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("transactions", data)
        self.assertLessEqual(len(data["transactions"]), 10)

    def test_delete_payments_non_existent_id(self):
        non_existent_id = "non-existent-id"
        response = requests.delete(f"{BASE_URL}/payments/{non_existent_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Payment ID not found", response.text)

if __name__ == '__main__':
    unittest.main()
