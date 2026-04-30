import pytest
import requests

# Test Case 3: Validate behavior when attempting to cancel a payment with a non-existent ID

def test_cancel_payment_nonexistent_id():
    payment_id = "nonexistent123"  # Example of a non-existent payment ID
    url = f"https://api.example.com/payments/{payment_id}"  # Replace with the actual payments endpoint URL
    response = requests.delete(url)
    assert response.status_code == 404  # Assuming 404 Not Found for non-existent resource
    assert "error" in response.json()
    assert response.json()["error"] == "Payment ID not found"  # Adjust based on actual error message
