import numpy as np

# Currency specific rules for min and max payment amounts, extendable
CURRENCY_RULES = {
    'USD': {'min': 10, 'max': 1000},
    'EUR': {'min': 20, 'max': 1500},
    'GBP': {'min': 5, 'max': 800},
    'JPY': {'min': 1000, 'max': 100000},
    'AUD': {'min': 15, 'max': 1200},
    'CAD': {'min': 10, 'max': 1100},
}

# Default edge cases and probability
DEFAULT_EDGE_CASES = [0, 1, 999999]
DEFAULT_EDGE_CASE_PROBABILITY = 0.05  # 5% chance for edge cases


def generate_amount(
    currency='USD',
    distribution='normal',
    mean=100,
    std_dev=50,
    low=10,
    high=1000,
    edge_cases=None,
    edge_case_probability=None,
    decimal_precision=0
):
    """
    Generate a synthetic payment amount based on distribution and currency rules.

    Args:
        currency (str): Currency code to apply min/max rules.
        distribution (str): Distribution type ('normal', 'uniform', 'exponential', 'lognormal').
        mean (float): Mean for normal distribution.
        std_dev (float): Standard deviation for normal distribution.
        low (float): Lower bound for uniform distribution or scale for exponential.
        high (float): Upper bound for uniform distribution.
        edge_cases (list): List of edge cases to include.
        edge_case_probability (float): Probability of selecting an edge case.
        decimal_precision (int): Number of decimal places for the result.

    Returns:
        float: Synthetic payment amount.
    """
    if edge_cases is None:
        edge_cases = DEFAULT_EDGE_CASES
    if edge_case_probability is None:
        edge_case_probability = DEFAULT_EDGE_CASE_PROBABILITY

    # Input validation
    if decimal_precision < 0:
        raise ValueError("decimal_precision must be non-negative")
    if not (0 <= edge_case_probability <= 1):
        raise ValueError("edge_case_probability must be between 0 and 1")

    # Edge case inclusion
    if np.random.rand() < edge_case_probability:
        amount = float(np.random.choice(edge_cases))
    else:
        # Generate amount based on distribution
        if distribution == 'uniform':
            amount = np.random.uniform(low, high)
        elif distribution == 'exponential':
            amount = np.random.exponential(scale=low)
        elif distribution == 'lognormal':
            amount = np.random.lognormal(mean=mean, sigma=std_dev)
        else:  # default to normal
            amount = np.random.normal(mean, std_dev)

    # Apply currency specific min/max rules
    rules = CURRENCY_RULES.get(currency, {'min': 10, 'max': 1000})
    min_val, max_val = rules['min'], rules['max']

    # Clamp amount within min and max
    amount = max(min_val, min(amount, max_val))

    # Round to specified decimal precision
    return round(amount, decimal_precision)


# Example usage:
# print(generate_amount(currency='EUR', distribution='normal', mean=200, std_dev=80, decimal_precision=2))
# print(generate_amount(currency='GBP', distribution='uniform', low=5, high=800))
# print(generate_amount(currency='JPY', distribution='exponential', low=1000))
# print(generate_amount(currency='AUD', distribution='lognormal', mean=4, std_dev=0.5, decimal_precision=2))
