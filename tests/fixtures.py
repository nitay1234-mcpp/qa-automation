import pytest
from typing import List, Dict, Any
from faker import Faker
import random
import numpy as np

fake = Faker()

@pytest.fixture
def get_valid_amounts() -> List[float]:
    """Returns a list of valid payment amounts for testing, including edge cases."""
    return [0.01, 100, 500, 1000, 150.50, 9999, 999999, 0.05, 2500]  # Added more edge cases

@pytest.fixture
def get_invalid_amounts() -> List[Any]:
    """Returns a list of invalid payment amounts for testing, including edge cases."""
    return [None, -50, 0, 'abc', 1000001, '', '-1.99', float('inf'), -float('inf'), '   ', '0.01abc']  # Categorized invalid inputs

@pytest.fixture
def get_user_profiles() -> List[Dict[str, Any]]:
    """Returns a list of user profiles with improved payment histories for realistic testing."""
    def generate_payments(mean=100, stddev=50, count=5):
        """Generates payment amounts based on a normal distribution, clipped to positive values."""
        payments = np.random.normal(mean, stddev, count)
        payments = [round(p, 2) for p in payments if p > 0]
        return payments if payments else [mean]  # fallback if all negative

    return [
        {'user_id': 1, 'user_type': 'new', 'payment_history': []},
        {'user_id': 2, 'user_type': 'repeat', 'payment_history': generate_payments(mean=100, stddev=30, count=10)},
        {'user_id': 3, 'user_type': 'mid-tier', 'payment_history': generate_payments(mean=500, stddev=200, count=8)},
        {'user_id': 4, 'user_type': 'high-value', 'payment_history': generate_payments(mean=10000, stddev=3000, count=3)},
        {'user_id': 5, 'user_type': 'inactive', 'payment_history': [0, -5, 0, -10]},  # Simulating failed payments
        {'user_id': 6, 'user_type': 'fraudulent', 'payment_history': [200000, 150000, 300000]},  # Suspicious high payments
        {'user_id': 7, 'user_type': 'fraudulent-pattern', 'payment_history': [random.choice([0, 1000, 5000, 0, 0]) for _ in range(10)]},  # Erratic payments
        {'user_id': 8, 'user_type': 'new', 'payment_history': [], 'email': fake.email(), 'name': fake.name()},
        {'user_id': 9, 'user_type': 'new', 'payment_history': [], 'email': fake.email(), 'name': fake.name()},
    ]

@pytest.fixture(params=[0.01, 100, 500, 1000, 2500])
def valid_amount(request) -> float:
    """Provides various valid payment amounts for testing."""
    return request.param
