import pytest
import requests

# Test Case 3-020: Validate behavior when attempting to cancel a payment without providing a payment ID

def test_cancel_payment_missing_id():
    url = "https://api.example.com/payments/"  # Replace with the actual payments endpoint URL
    response = requests.delete(url)  # No payment ID provided in URL
    
    # Assuming the API returns 400 Bad Request for missing payment ID
    assert response.status_code == 400
    data = response.json()
    assert data.get("error") is not None
    assert "missing payment id" in data.get("error").lower() or "invalid request" in data.get("error").lower()
