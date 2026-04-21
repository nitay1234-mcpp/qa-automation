# Test Fixtures for Payment Processing Tests

import pytest

@pytest.fixture
def valid_amounts():
    return [100, 500, 1000, 150.50, 9999]

@pytest.fixture
def invalid_amounts():
    return [None, -50, 0, 'abc', 1000001, '', '-1.99']

@pytest.fixture
def user_profiles():
    return [
        {'user_id': 1, 'user_type': 'new', 'payment_history': []},
        {'user_id': 2, 'user_type': 'repeat', 'payment_history': [100, 200]},
        {'user_id': 3, 'user_type': 'high-value', 'payment_history': [10000, 20000]},
    ]
