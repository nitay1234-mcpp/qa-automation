import unittest
import requests

class TestDeletePayments(unittest.TestCase):
    BASE_URL = "http://example.com/api"

    def test_cancel_with_non_existent_id(self):
        non_existent_id = "invalid_id_123"
        url = f"{self.BASE_URL}/payments/{non_existent_id}"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Payment not found", response.text)

if __name__ == "__main__":
    unittest.main()
