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
    (-1, 'Invalid amount'),  # Very small negative
    (-50, 'Invalid amount'),  # Invalid amount
    (0, 'Invalid amount'),  # Zero amount
    (0.00, 'Invalid amount'),  # Zero amount as decimal
    (9999.99, None),  # Maximum valid decimal payment
    (10000.01, 'Amount exceeds limit'),  # Just over the limit
    (1000000, 'Amount exceeds limit'),  # Exceeds maximum payment limit
    (-100, 'Invalid amount'),  # Negative amount
    ('abc', 'Invalid amount'),  # Non-numeric string
    ('   100', None),  # Whitespace
    ('100.00abc', 'Invalid amount'),  # Non-numeric with text
    (None, 'Invalid amount'),  # None amount
    ('', 'Invalid amount'),  # Empty string
    ('-1.99', 'Invalid amount'),  # Negative decimal
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

@pytest.mark.parametrize('card_info, expected_error', [
    ({'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
    ({'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
    ({'number': '4111111111111111', 'cvv': '123', 'expiry': '01/21'}, None),  # Valid card
    ({'number': '4111111111111111', 'cvv': '12a'}, 'Invalid CVV'),  # Invalid format
    ({'number': '4111111111111111', 'cvv': '123', 'expiry': '01/19'}, 'Card expired'),  # Expired card
])
def test_payment_processing_invalid_card(page: Page, card_info, expected_error):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Card number"]', card_info['number'])
    page.fill('[aria-label="CVV"]', card_info['cvv'])
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Invalid Card Processing", {"card_info": card_info, "expected_error": expected_error})

# Other tests remain unchanged
