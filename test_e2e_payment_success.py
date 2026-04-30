import pytest
import requests
import time

API_BASE_URL = "https://api.your-payment-gateway.com"  # Replace with actual payment gateway API base URL

@pytest.fixture
    def valid_payment_data():
        return {
            "payment_method": "credit_card",
            "card_number": "4111111111111111",
            "expiry_date": "12/25",
            "cvv": "123",
            "amount": 100.00,
            "currency": "USD"
        }


def test_e2e_successful_payment(valid_payment_data):
    # Simulate sending payment request to real payment gateway
    response = requests.post(f"{API_BASE_URL}/payments", json=valid_payment_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    assert "transaction_id" in data

    transaction_id = data["transaction_id"]

    # Poll payment status endpoint to confirm transaction success
    for _ in range(5):  # retry up to 5 times with delay
        status_response = requests.get(f"{API_BASE_URL}/payments/{transaction_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        if status_data.get("status") == "success":
            break
        time.sleep(2)
    else:
        pytest.fail("Payment did not reach success status within expected time")


def test_e2e_payment_webhook_processing():
    # Simulate receiving a payment success webhook event from payment gateway
    webhook_payload = {
        "event": "payment_success",
        "data": {
            "transaction_id": "test_txn_12345",
            "amount": 100.00,
            "currency": "USD",
            "status": "success"
        }
    }

    response = requests.post(f"{API_BASE_URL}/webhook/payment", json=webhook_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("result") == "processed"

    # Optionally verify internal system state or database for transaction status update
    # This will depend on your system's API or database access
