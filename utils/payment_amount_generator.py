import numpy as np

# Currency specific rules for min and max payment amounts
CURRENCY_RULES = {
    'USD': {'min': 10, 'max': 1000},
    'EUR': {'min': 20, 'max': 1500},
    'GBP': {'min': 5, 'max': 800},
}

# Edge cases to include in synthetic data generation
EDGE_CASES = [0, 1, 999999]
EDGE_CASE_PROBABILITY = 0.05  # 5% chance for edge cases


def generate_amount(currency='USD', distribution='normal', mean=100, std_dev=50, low=10, high=1000):
    """
    Generate a synthetic payment amount based on distribution and currency rules.

    Args:
        currency (str): Currency code to apply min/max rules.
        distribution (str): Distribution type ('normal' or 'uniform').
        mean (float): Mean for normal distribution.
        std_dev (float): Standard deviation for normal distribution.
        low (float): Lower bound for uniform distribution.
        high (float): Upper bound for uniform distribution.

    Returns:
        int: Synthetic payment amount.
    """
    # Edge case inclusion
    if np.random.rand() < EDGE_CASE_PROBABILITY:
        return np.random.choice(EDGE_CASES)

    # Generate amount based on distribution
    if distribution == 'uniform':
        amount = np.random.uniform(low, high)
    else:  # default to normal
        amount = np.random.normal(mean, std_dev)

    # Apply currency specific min/max rules
    rules = CURRENCY_RULES.get(currency, {'min': 10, 'max': 1000})
    min_val, max_val = rules['min'], rules['max']

    # Clamp amount within min and max
    amount = max(min_val, min(amount, max_val))

    # Round to nearest integer
    return int(round(amount))


# Example usage:
# print(generate_amount(currency='EUR', distribution='normal', mean=200, std_dev=80))
# print(generate_amount(currency='GBP', distribution='uniform', low=5, high=800))
