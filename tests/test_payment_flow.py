import pytest
from playwright.sync_api import Page
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.mark.parametrize('amount, expected_error', [
    (100, None),  # Valid payment
    (-50, 'Invalid amount'),  # Invalid amount
    (0, 'Invalid amount'),  # Zero amount
    (None, 'Invalid amount')  # None amount
])
def test_payment_flow(page: Page, amount, expected_error):
    page.goto('https://staging.novapay.io/checkout')
    if amount is not None:
        page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')

    if expected_error:
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        assert expected_error in page.locator('.error-message').inner_text()
        log_event("Payment Error", {"amount": amount, "error": expected_error, "timestamp": datetime.now()})
    else:
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
        log_event("Payment Success", {"amount": amount, "timestamp": datetime.now()})


def test_payment_with_network_failure(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    # Simulate network failure
    page.route('**/*', lambda route: route.abort())
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message
    log_event("Network Failure", {"amount": 100, "timestamp": datetime.now()})

# Additional test cases can be similarly enhanced
