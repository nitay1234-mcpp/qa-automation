import pytest
import requests

BASE_URL = "http://example.com/api"  # Replace with actual base URL

# Transaction History Retrieval Additional Tests

def test_transaction_history_with_invalid_date_format():
    params = {
        "start_date": "2023-13-01",  # Invalid month
        "end_date": "2023-12-31",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_transaction_history_with_end_date_before_start_date():
    params = {
        "start_date": "2023-12-31",
        "end_date": "2023-01-01",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_transaction_history_with_no_results():
    params = {
        "start_date": "1900-01-01",
        "end_date": "1900-01-02",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)
    assert len(data["transactions"]) == 0


def test_transaction_history_with_invalid_pagination():
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "page": -1,  # Invalid page
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


# Cancel Payment Additional Tests

def test_cancel_payment_valid_id():
    valid_payment_id = "valid123"  # Replace with a valid payment ID for real test
    response = requests.delete(f"{BASE_URL}/payments/{valid_payment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "cancelled" or response.status_code == 204


def test_cancel_payment_missing_id():
    url = f"{BASE_URL}/payments/"  # No payment ID in URL
    response = requests.delete(url)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_cancel_payment_malformed_id():
    malformed_id = "!!!@@@###"
    response = requests.delete(f"{BASE_URL}/payments/{malformed_id}")
    assert response.status_code == 400 or response.status_code == 404
    data = response.json()
    assert "error" in data


def test_cancel_payment_service_unavailable(monkeypatch):
    # Monkeypatch requests.delete to simulate a 503 Service Unavailable response
    class MockResponse:
        def __init__(self):
            self.status_code = 503
        def json(self):
            return {"error": "Service Unavailable"}

    def mock_delete(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "delete", mock_delete)

    payment_id = "anyid"
    response = requests.delete(f"{BASE_URL}/payments/{payment_id}")
    assert response.status_code == 503
    data = response.json()
    assert "error" in data
