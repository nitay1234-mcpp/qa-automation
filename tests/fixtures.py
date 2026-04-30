# Test Fixtures for Payment Processing Tests

import pytest
from typing import List, Dict, Any
from faker import Faker

fake = Faker()

@pytest.fixture
def get_valid_amounts() -> List[float]:
    """Returns a list of valid payment amounts for testing, including edge cases."""
    return [
        0.001, 0.01, 0.05, 0.995, 1.005, 100, 500, 1000, 150.50, 9999, 999999, 2500,
        1e-7,  # Very small positive value
        1e7,   # Very large value
    ]  # Added more edge cases including rounding and precision

@pytest.fixture
def get_invalid_amounts() -> List[Any]:
    """Returns a list of invalid payment amounts for testing, including edge cases."""
    return [
        None, -50, 0, 'abc', 1000001, '', '-1.99', float('inf'), -float('inf'), '   ', '0.01abc',
        True, False, [], {},
        '1 000', '12,34', '$100',
        -1e-7,  # Very small negative value
        1e100,  # Extremely large number
        '\ud83d\ude00',  # Unicode emoji
    ]  # Categorized invalid inputs and more edge cases

@pytest.fixture
def get_user_profiles() -> List[Dict[str, Any]]:
    """Returns a list of user profiles with varying payment histories and edge cases."""
    return [
        {'user_id': 0, 'user_type': 'new', 'payment_history': []},  # Boundary user_id
        {'user_id': 1, 'user_type': 'new', 'payment_history': []},
        {'user_id': 2, 'user_type': 'repeat', 'payment_history': [100, 200]},
        {'user_id': 3, 'user_type': 'high-value', 'payment_history': [10000, 20000]},
        {'user_id': 4, 'user_type': 'inactive', 'payment_history': [50, 75, 40]},  # User with failed payments
        {'user_id': 5, 'user_type': 'new', 'payment_history': [], 'email': fake.email(), 'name': fake.name()},  # Randomized user
        {'user_id': 6, 'user_type': 'fraudulent', 'payment_history': [200000]},  # User with suspicious high payments
        {'user_id': 7, 'user_type': 'new', 'payment_history': [], 'email': fake.email(), 'name': fake.name()},  # Another randomized user
        {'user_id': -1, 'user_type': None, 'payment_history': None},  # Missing fields and negative id
        {'user_id': 8, 'user_type': 'repeat', 'payment_history': [0, -10, 100]},  # Payment history with invalid values
        {'user_id': 9, 'user_type': 'special', 'payment_history': [100], 'name': 'José 🚀', 'email': 'josé@example.com'},  # Unicode and special chars
        {'user_id': 10, 'user_type': 'large-history', 'payment_history': list(range(1000))},  # Large payment history
    ]

@pytest.fixture(params=[0.001, 0.01, 0.05, 0.995, 1.005, 100, 500, 1000, 2500])
def valid_amount(request) -> float:
    """Provides various valid payment amounts for testing."""
    return request.param
