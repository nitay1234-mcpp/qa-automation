import pytest
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.mark.parametrize('payment_method, amount, expected_error', [
    ('paypal', 100, None),  # Valid PayPal payment
    ('credit_card', -1, 'Invalid amount'),  # Invalid amount
    ('credit_card', 10000.01, 'Amount exceeds limit'),  # Exceeds maximum payment limit
])
def test_multiple_payment_methods(navigate_to_checkout, payment_method, amount, expected_error):
    page = navigate_to_checkout
    if payment_method == 'paypal':
        page.click('button[aria-label="PayPal"]')
    else:
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

@pytest.mark.parametrize('payment_method, expected_message', [
    ('bank_transfer', 'Bank transfer selected'),
    ('digital_wallet', 'Digital wallet selected'),
])
def test_other_payment_methods(navigate_to_checkout, payment_method, expected_message):
    page = navigate_to_checkout
    page.click(f'button[aria-label="{payment_method.replace("_", " ").title()}"]')
    page.wait_for_selector('.payment-method-confirmation')
    assert expected_message in page.locator('.payment-method-confirmation').inner_text()
    log_event("Payment Method Selection", {"method": payment_method, "timestamp": datetime.now()})

@pytest.mark.parametrize('payment_method, expected_message', [
    ('apple_pay', 'Apple Pay selected'),
    ('google_pay', 'Google Pay selected'),
])
def test_additional_payment_methods(navigate_to_checkout, payment_method, expected_message):
    page = navigate_to_checkout
    page.click(f'button[aria-label="{payment_method.replace("_", " ").title()}"]')
    page.wait_for_selector('.payment-method-confirmation')
    assert expected_message in page.locator('.payment-method-confirmation').inner_text()
    log_event("Payment Method Selection", {"method": payment_method, "timestamp": datetime.now()})
