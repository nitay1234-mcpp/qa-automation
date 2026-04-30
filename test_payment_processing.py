import pytest
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPaymentProcessing:

    # Existing tests omitted for brevity

    def test_concurrent_payments(self):
        logger.info("Testing concurrency for payment processing.")
        processor = PaymentProcessor()
        num_threads = 20

        def make_payment():
            return processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_payment) for _ in range(num_threads)]
            results = [future.result() for future in futures]

        success_count = sum(1 for r in results if r['status'] == 'success')
        logger.info(f"Concurrent success count: {success_count} out of {num_threads}")
        assert success_count == num_threads, "Not all concurrent payments succeeded"

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (0, {'number': '4111111111111111', 'cvv': '123'}, 'error'),  # Zero amount
        (-10, {'number': '4111111111111111', 'cvv': '123'}, 'error'),  # Negative amount
        (100, {'number': '4111111111111111', 'cvv': '12'}, 'error'),  # Invalid CVV length
        (100, {'number': '', 'cvv': '123'}, 'error'),  # Empty card number
        (100, {'number': '4111111111111111', 'cvv': ''}, 'error'),  # Empty CVV
    ])
    def test_edge_cases(self, amount, card_info, expected_status):
        logger.info(f"Testing edge case with amount: {amount}, card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        logger.debug(f"Edge case response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"
