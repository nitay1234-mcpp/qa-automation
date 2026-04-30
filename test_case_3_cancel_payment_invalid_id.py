import pytest
import requests

BASE_URL = "http://example.com/api"  # Replace with actual base URL

@pytest.fixture
    def invalid_payment_id():
        return "non_existent_id"


def test_cancel_payment_with_invalid_id(invalid_payment_id):
    response = requests.delete(f"{BASE_URL}/payments/{invalid_payment_id}")
    assert response.status_code == 404
    data = response.json()
    assert data.get("error") is not None
    assert "not found" in data.get("error").lower()
