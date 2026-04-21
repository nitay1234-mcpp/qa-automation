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
    (None, 'Invalid amount'),  # None amount
    ('abc', 'Invalid amount'),  # Non-numeric string
    (1000000, 'Amount exceeds limit'),  # Exceeds maximum payment limit
    (-100, 'Invalid amount'),  # Negative amount
    ('', 'Invalid amount'),  # Empty string
    ('-1.99', 'Invalid amount'),  # Negative decimal
    (150.50, None),  # Valid decimal payment
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

@pytest.mark.parametrize('amount', [
    (500),  # Valid payment
    (1000),  # Higher valid payment
    (9999),  # Maximum boundary payment
    (1.99),  # Valid payment with cents
])
def test_valid_payment_scenarios(page: Page, amount):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Payment Success", {"amount": amount, "timestamp": datetime.now()})

# Test for processing payment with invalid card details
@pytest.mark.parametrize('card_info, expected_error', [
    ({'number': '1234567890123456', 'cvv': '123'}, 'fraud_detected'),
    ({'number': '4111111111111111', 'cvv': '999', 'expiry': '01/20'}, 'error'),  # Invalid CVV
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

# Test for retrieving transaction history with filters
def test_retrieve_transaction_history(page: Page):
    page.goto('https://staging.novapay.io/transaction-history')
    page.fill('[aria-label="Date From"]', '2023-01-01')
    page.fill('[aria-label="Date To"]', '2023-12-31')
    page.click('button[type="submit"]')
    page.wait_for_selector('.transaction-list')
    assert page.locator('.transaction-list').is_visible()
    log_event("Transaction History Retrieved", {"filters": {"date_from": '2023-01-01', "date_to": '2023-12-31'}})

# Test for canceling a payment with a valid ID
def test_cancel_payment_success(page: Page):
    page.goto('https://staging.novapay.io/payments')
    page.fill('[aria-label="Payment ID"]', 'valid_payment_id')
    page.click('button[type="cancel"]')
    page.wait_for_selector('.cancel-success')
    assert page.locator('.cancel-success').is_visible()
    log_event("Payment Canceled", {"payment_id": 'valid_payment_id'})

# Test for invalid Payment ID cancellation
def test_cancel_payment_invalid_id(page: Page):
    page.goto('https://staging.novapay.io/payments')
    page.fill('[aria-label="Payment ID"]', 'invalid_payment_id')
    page.click('button[type="cancel"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    log_event("Invalid Payment ID Cancellation Attempted", {"payment_id": 'invalid_payment_id'})

# Test for non-existent Payment ID cancellation
def test_cancel_payment_non_existent_id(page: Page):
    page.goto('https://staging.novapay.io/payments')
    page.fill('[aria-label="Payment ID"]', 'non_existent_payment_id')
    page.click('button[type="cancel"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    log_event("Non-existent Payment ID Cancellation Attempted", {"payment_id": 'non_existent_payment_id'})

# Test for invalid amount scenarios
@pytest.mark.parametrize('amount, expected_error', [
    (-50, 'Invalid amount'),
    (0, 'Invalid amount'),
    (None, 'Invalid amount'),
    ('abc', 'Invalid amount'),
])
def test_invalid_amount_scenarios(page: Page, amount, expected_error):
    page.goto('https://staging.novapay.io/checkout')
    if amount is not None:
        page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Invalid Amount Error", {"amount": amount, "expected_error": expected_error})
