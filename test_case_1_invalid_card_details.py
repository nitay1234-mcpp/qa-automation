import pytest
import requests

# Test Case 1: Validate error message for processing payment with invalid card details

def test_invalid_card_details():
    url = "https://api.example.com/payments"  # Replace with the actual payments endpoint URL
    invalid_payment_data = {
        "card_number": "1234567890123456",
        "expiry_date": "01/20",
        "cvv": "123",
        "amount": 100.00
    }
    response = requests.post(url, json=invalid_payment_data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid card details"  # Adjust based on actual error message
