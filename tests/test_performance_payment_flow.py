import pytest
from playwright.sync_api import Page
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.fixture
def navigate_to_checkout(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    return page

# Helper function to perform a payment
def perform_payment(page: Page, amount: float):
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Payment Success", {"amount": amount, "timestamp": datetime.now()})

# Load test with concurrent payments
@pytest.mark.parametrize('num_concurrent_payments', [10, 50, 100])
def test_load_payment_requests(navigate_to_checkout, num_concurrent_payments):
    page = navigate_to_checkout

    def task(amount):
        # Each thread uses the same page object for simplicity
        perform_payment(page, amount)

    amounts = [100 + i for i in range(num_concurrent_payments)]

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_payments) as executor:
        executor.map(task, amounts)
    end_time = time.time()

    duration = end_time - start_time
    log_event("Load Test", {"num_requests": num_concurrent_payments, "duration_seconds": duration, "timestamp": datetime.now()})
    assert duration < 60, f"Load test exceeded time limit with duration {duration} seconds"

# Response time benchmark test
@pytest.mark.parametrize('amount', [100, 500, 1000])
def test_response_time_benchmark(navigate_to_checkout, amount):
    page = navigate_to_checkout

    start_time = time.time()
    perform_payment(page, amount)
    end_time = time.time()

    response_time = end_time - start_time
    log_event("Response Time", {"amount": amount, "response_time_seconds": response_time, "timestamp": datetime.now()})

    assert response_time < 10, f"Response time {response_time} seconds exceeded acceptable threshold"

