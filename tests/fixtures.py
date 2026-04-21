# Test Fixtures for Payment Processing Tests

import pytest
from typing import List, Dict, Any

@pytest.fixture
def get_valid_amounts() -> List[float]:
    """Returns a list of valid payment amounts for testing."""
    return [100, 500, 1000, 150.50, 9999]

@pytest.fixture
def get_invalid_amounts() -> List[Any]:
    """Returns a list of invalid payment amounts for testing."""
    return [None, -50, 0, 'abc', 1000001, '', '-1.99']

@pytest.fixture
def get_user_profiles() -> List[Dict[str, Any]]:
    """Returns a list of user profiles with varying payment histories."""
    return [
        {'user_id': 1, 'user_type': 'new', 'payment_history': []},
        {'user_id': 2, 'user_type': 'repeat', 'payment_history': [100, 200]},
        {'user_id': 3, 'user_type': 'high-value', 'payment_history': [10000, 20000]},
    ]
