import pytest
import requests

BASE_URL = "http://example.com/api"  # Replace with actual base URL

# Transaction History Enhanced Filters

def test_transaction_history_boundary_dates():
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data

@pytest.mark.parametrize("invalid_date", ["2023-13-01", "01-01-2023", "2023/01/01"])
def test_transaction_history_invalid_date_formats(invalid_date):
    params = {
        "start_date": invalid_date,
        "end_date": "2023-12-31",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 400  # Bad Request expected for invalid dates

def test_transaction_history_missing_filters():
    response = requests.get(f"{BASE_URL}/transactions")
    assert response.status_code == 400  # Assuming filters are required

def test_transaction_history_no_results():
    params = {
        "start_date": "1990-01-01",
        "end_date": "1990-12-31",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data.get("transactions") == []

def test_transaction_history_pagination_beyond_range():
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "page": 9999,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data.get("transactions") == []

# Cancel Payment Additional Scenarios

def test_cancel_payment_missing_id():
    response = requests.delete(f"{BASE_URL}/payments/")
    # Expected 404 or 400 depending on API implementation
    assert response.status_code in (400, 404)

@pytest.mark.parametrize("invalid_id", ["abc$%123", "123", ""])
def test_cancel_payment_invalid_id_format(invalid_id):
    response = requests.delete(f"{BASE_URL}/payments/{invalid_id}")
    assert response.status_code == 400  # Bad Request expected

def test_cancel_payment_success():
    valid_payment_id = "valid123"  # Replace with a valid payment ID for testing
    response = requests.delete(f"{BASE_URL}/payments/{valid_payment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "cancelled"

def test_cancel_payment_already_completed():
    completed_payment_id = "completed123"  # Replace with a payment ID in completed state
    response = requests.delete(f"{BASE_URL}/payments/{completed_payment_id}")
    assert response.status_code == 409  # Conflict expected for non-cancellable payment

def test_cancel_payment_unauthorized():
    valid_payment_id = "valid123"
    response = requests.delete(f"{BASE_URL}/payments/{valid_payment_id}", headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401  # Unauthorized expected
