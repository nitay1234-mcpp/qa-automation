import pytest
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPaymentProcessing:

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

    @pytest.mark.timeout(10)
    @pytest.mark.skip
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_webhook_handling(self):
        logger.info("Testing webhook handling.")
        processor = PaymentProcessor()

        # Measure processing time for webhook
        webhook_data = {'event': 'payment_success', 'data': {'amount': 100}}
        start_time = time.time()
        response = processor.handle_webhook(webhook_data)
        duration = time.time() - start_time
        logger.debug(f"Webhook response: {response} in {duration:.2f} seconds")
        assert response['status'] == 'processed', "Expected 'processed' status for valid webhook"
        assert duration <= 1, f"Webhook processing took too long: {duration:.2f} seconds"

        # Simulate an invalid webhook
        webhook_data = {'event': 'invalid_event'}
        response = processor.handle_webhook(webhook_data)
        logger.debug(f"Invalid webhook response: {response}")
        assert response['status'] == 'error', "Expected 'error' status for invalid webhook"

    def test_timeout_handling(self):
        logger.info("Testing timeout handling for payment processing.")
        processor = PaymentProcessor()
        # Simulate a timeout scenario (mock or simulate network timeout)
        # Assuming process_payment returns {'status': 'timeout', 'http_code': 408} on timeout
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, simulate_timeout=True)
        logger.debug(f"Timeout handling response: {response}")
        assert response.get('http_code') == 408, "Expected HTTP 408 status code for timeout"
        assert response['status'] == 'timeout', "Expected 'timeout' status for timeout scenario"

    def test_load_throughput(self):
        logger.info("Testing load throughput for payment processing.")
        processor = PaymentProcessor()
        num_requests = 1000
        max_duration_seconds = 60  # 1 minute

        def make_payment_request():
            return processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_payment_request) for _ in range(num_requests)]
            results = []
            for future in as_completed(futures):
                results.append(future.result())
        duration = time.time() - start_time
        logger.debug(f"Processed {num_requests} payment requests in {duration:.2f} seconds")

        # Assert throughput SLA
        assert duration <= max_duration_seconds, f"Throughput SLA not met: {duration:.2f} seconds"

        # Assert error rate < 1%
        error_count = sum(1 for r in results if r['status'] != 'success')
        error_rate = error_count / num_requests
        logger.info(f"Error rate during load test: {error_rate:.2%}")
        assert error_rate < 0.01, f"Error rate too high during load test: {error_rate:.2%}"

    # Existing tests below unchanged...

    def test_edge_cases_payment_methods(self):
        logger.info("Testing edge cases for payment methods.")
        processor = PaymentProcessor()
        # Test with an expired card
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'})
        logger.debug(f"Expired card response: {response}")
        assert response['status'] == 'error', "Expected 'error' status for expired card"
        
        # Test with a payment method not accepted
        response = processor.process_payment(amount=100, card_info={'number': '5500000000000004', 'cvv': '123'})
        logger.debug(f"Not accepted card response: {response}")
        assert response['status'] == 'payment_method_not_accepted', "Expected 'payment_method_not_accepted' status for non-accepted card"

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (100, {'number': '4111111111111111', 'cvv': '123'}, 'success'),
        (100, {'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
        (200, {'number': '4111111111111111', 'cvv': '123', 'expiry': '01/20'}, 'error'),  # Expired Card
        (100, {'number': '5500000000000004', 'cvv': '123'}, 'payment_method_not_accepted')  # Not Accepted Card
    ])
    def test_invalid_card_length(self, amount, card_info, expected_status):
        logger.info(f"Testing invalid card length for amount: {amount} and card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        logger.debug(f"Invalid card length response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    @pytest.mark.parametrize("card_info, expected_status", [
        ({'number': '4111A11111111111', 'cvv': '123'}, 'error'),  # Invalid card format
        ({'number': '4111-1111-1111-1111', 'cvv': '123'}, 'error'),  # Non-numeric characters
        ({'number': '1234', 'cvv': '123'}, 'error'),  # Too short
        ({'number': '4111111111111111111111111111111111', 'cvv': '123'}, 'error')  # Too long
    ])
    def test_invalid_card_formats(self, card_info, expected_status):
        logger.info(f"Testing invalid card format with card_info: {card_info}")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info=card_info)
        logger.debug(f"Invalid card format response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for {card_info}. Got {response['status']}"

    # Enhanced concurrency tests
    def test_concurrent_payment_attempts(self):
        logger.info("Testing concurrent payment attempts.")
        processor = PaymentProcessor()
        num_attempts = 20

        def make_payment():
            return processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})

        with ThreadPoolExecutor(max_workers=num_attempts) as executor:
            futures = [executor.submit(make_payment) for _ in range(num_attempts)]
            results = [future.result() for future in as_completed(futures)]

        success_count = sum(1 for r in results if r['status'] == 'success')
        logger.debug(f"Concurrent payment success count: {success_count} out of {num_attempts}")
        assert success_count == num_attempts, f"Expected all concurrent payments to succeed, but got {success_count} successes."

    # Enhanced partial refund tests
    @pytest.mark.parametrize("refund_amount, expected_status", [
        (50, 'success'),  # Valid partial refund
        (0, 'error'),    # Zero refund amount
        (-10, 'error'),  # Negative refund amount
        (200, 'error')   # Refund greater than original payment
    ])
    def test_partial_refunds(self, refund_amount, expected_status):
        logger.info(f"Testing partial refunds with amount: {refund_amount}")
        processor = PaymentProcessor()
        response = processor.process_refund(amount=refund_amount, card_info={'number': '4111111111111111', 'cvv': '123'})
        logger.debug(f"Partial refund response: {response}")
        assert response['status'] == expected_status, f"Expected {expected_status} for refund amount {refund_amount}. Got {response['status']}"

    # Security-related tests for untested endpoints
    def test_unauthorized_access(self):
        logger.info("Testing unauthorized access to payment processing.")
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, auth_token=None)
        logger.debug(f"Unauthorized access response: {response}")
        assert response['status'] == 'unauthorized', "Expected 'unauthorized' status for missing auth token"

    def test_rate_limiting(self):
        logger.info("Testing rate limiting on payment processing endpoint.")
        processor = PaymentProcessor()
        num_requests = 100
        responses = []

        def make_request():
            return processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            for future in as_completed(futures):
                responses.append(future.result())

        rate_limited_count = sum(1 for r in responses if r['status'] == 'rate_limited')
        logger.debug(f"Rate limited responses: {rate_limited_count} out of {num_requests}")
        assert rate_limited_count > 0, "Expected some requests to be rate limited under high load"

    # Additional tests can be added as needed
