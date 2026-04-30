import pytest
import requests

BASE_URL = "http://example.com/api"  # Replace with actual base URL

@pytest.fixture
    def valid_filters():
        return {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "status": "completed",
            "page": 1,
            "page_size": 10
        }


def test_retrieve_transaction_history_with_valid_filters(valid_filters):
    response = requests.get(f"{BASE_URL}/transactions", params=valid_filters)
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)
    # Additional assertions for pagination
    assert data.get("page") == valid_filters["page"]
    assert data.get("page_size") == valid_filters["page_size"]
