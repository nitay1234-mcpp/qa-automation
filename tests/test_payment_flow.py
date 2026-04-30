import pytest
from playwright.sync_api import Page
import logging
from datetime import datetime
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.fixture
def navigate_to_checkout(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    return page

# Existing test cases...

# Improved test case for handling multiple payment methods
@pytest.mark.parametrize('payment_method, amount, payment_details, expected_error', [
    ('paypal', 100, None, None),
    ('credit_card', 100, {'card_number': '4111111111111111', 'cvv': '123', 'expiry': '12/25'}, None),
    ('credit_card', -1, {'card_number': '4111111111111111', 'cvv': '123', 'expiry': '12/25'}, 'Invalid amount'),
    ('apple_pay', 50, None, None),
    # Add more cases as needed
])
def test_multiple_payment_methods_enhanced(navigate_to_checkout, payment_method, amount, payment_details, expected_error):
    page = navigate_to_checkout

    def select_payment_method(method):
        page.click(f'button[aria-label="{method.replace("_", " ").title()}"]')

    def fill_payment_details(details):
        if details:
            page.fill('[aria-label="Card Number"]', details.get('card_number', ''))
            page.fill('[aria-label="CVV"]', details.get('cvv', ''))
            page.fill('[aria-label="Expiry Date"]', details.get('expiry', ''))

    select_payment_method(payment_method)
    if amount is not None:
        page.fill('[aria-label="Payment amount"]', str(amount))
    fill_payment_details(payment_details)
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

# Other existing test cases remain unchanged
