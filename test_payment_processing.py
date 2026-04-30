import pytest
import logging
import time
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPaymentProcessing:

    def generate_random_amount(self):
        # Generate a payment amount using log-normal distribution to simulate real-world payment amounts
        amount = np.random.lognormal(mean=4, sigma=1.0)  # mean and sigma can be tuned
        # Clamp amount to a sensible range
        amount = max(1, min(amount, 10000))
        return round(amount, 2)

    def generate_random_card_info(self):
        # Dummy card info generator for testing
        card_numbers = [
            '4111111111111111',  # Valid
            '1234567890123456',  # Fraud
            '5500000000000004'   # Not accepted
        ]
        cvvs = ['123', '999', '321']
        expiries = ['12/25', '01/20', '11/24']
        card_info = {
            'number': random.choice(card_numbers),
            'cvv': random.choice(cvvs),
            'expiry': random.choice(expiries)
        }
        return card_info

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_payment_processing_randomized(self):
        processor = PaymentProcessor()
        for _ in range(10):  # Test 10 random payments
            amount = self.generate_random_amount()
            card_info = self.generate_random_card_info()
            logger.info(f"Processing payment for randomized amount: {amount} with card_info: {card_info}")
            start_time = time.time()
            response = processor.process_payment(amount=amount, card_info=card_info)
            duration = time.time() - start_time
            logger.debug(f"Received response: {response} in {duration:.2f} seconds")
            assert response['status'] in ['success', 'fraud_detected', 'error', 'payment_method_not_accepted'], 
                f"Unexpected status {response['status']}"
            assert duration <= 2, f"Payment processing took too long: {duration:.2f} seconds"

    # Existing tests below unchanged...

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (100, {'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
        (100, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_payment_processing(self, amount, card_info, expected_status):
        logger.info(f"Processing payment for amount: {amount} with card_info: {card_info}")
        processor = PaymentProcessor()
        start_time = time.time()
        response = processor.process_payment(amount=amount, card_info=card_info)
        duration = time.time() - start_time
        logger.debug(f"Received response: {response} in {duration:.2f} seconds")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"
        # SLA: 95% of requests within 2 seconds (relaxed here for single test)
        assert duration <= 2, f"Payment processing took too long: {duration:.2f} seconds"

    # ... other existing tests unchanged ...
