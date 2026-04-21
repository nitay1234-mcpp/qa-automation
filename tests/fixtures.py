# Test Fixtures for Payment Processing Tests

import pytest
from typing import List, Dict, Any
from faker import Faker

fake = Faker()

@pytest.fixture
def get_valid_amounts() -> List[float]:
    """Returns a list of valid payment amounts for testing, including edge cases."""
    return [0.01, 100, 500, 1000, 150.50, 9999, 999999]

@pytest.fixture
def get_invalid_amounts() -> List[Any]:
    """Returns a list of invalid payment amounts for testing, including edge cases."""
    return [None, -50, 0, 'abc', 1000001, '', '-1.99', float('inf'), -float('inf'), '   ']

@pytest.fixture
def get_user_profiles() -> List[Dict[str, Any]]:
    """Returns a list of user profiles with varying payment histories."""
    return [
        {'user_id': 1, 'user_type': 'new', 'payment_history': []},
        {'user_id': 2, 'user_type': 'repeat', 'payment_history': [100, 200]},
        {'user_id': 3, 'user_type': 'high-value', 'payment_history': [10000, 20000]},
        {'user_id': 4, 'user_type': 'inactive', 'payment_history': [50, 75, 40]},  # User with failed payments
        {'user_id': 5, 'user_type': 'new', 'payment_history': [], 'email': fake.email(), 'name': fake.name()},  # Randomized user
    ]

@pytest.fixture(params=[0.01, 100, 500, 1000])
def valid_amount(request) -> float:
    """Provides various valid payment amounts for testing."""
    return request.param
