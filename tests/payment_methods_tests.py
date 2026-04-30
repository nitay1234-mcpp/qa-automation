import pytest
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

# Note: The navigate_to_checkout fixture is assumed to navigate to the checkout page and provide a page object

@pytest.mark.parametrize('payment_method, amount, expected_error', [
    ('paypal', 100, None),  # Valid PayPal payment
    ('credit_card', -1, 'Invalid amount'),  # Invalid amount
    ('credit_card', 10000.01, 'Amount exceeds limit'),  # Exceeds maximum payment limit
    ('credit_card', 0, 'Invalid amount'),  # Boundary test: zero amount
    ('credit_card', 10000, None),  # Boundary test: max allowed amount
])
def test_multiple_payment_methods(navigate_to_checkout, payment_method, amount, expected_error):
    """Test payment processing using multiple payment methods including boundary and error cases."""
    page = navigate_to_checkout
    if payment_method == 'paypal':
        page.click('button[aria-label="PayPal"]')
    else:
        page.fill('[aria-label="Payment amount"]', str(amount))
        page.click('button[type="submit"]')

    if expected_error:
        # Negative test: error message appears
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        assert expected_error in page.locator('.error-message').inner_text()
        log_event("Payment Error", {"amount": amount, "error": expected_error, "timestamp": datetime.now()})
    else:
        # Positive test: payment success message appears
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
        log_event("Payment Success", {"amount": amount, "timestamp": datetime.now()})

@pytest.mark.parametrize('payment_method, expected_message', [
    ('bank_transfer', 'Bank transfer selected'),
    ('digital_wallet', 'Digital wallet selected'),
])
def test_other_payment_methods(navigate_to_checkout, payment_method, expected_message):
    """Test selection and confirmation of other payment methods like bank transfer and digital wallet."""
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
    """Test selection and confirmation of additional payment methods like Apple Pay and Google Pay."""
    page = navigate_to_checkout
    page.click(f'button[aria-label="{payment_method.replace("_", " ").title()}"]')
    page.wait_for_selector('.payment-method-confirmation')
    assert expected_message in page.locator('.payment-method-confirmation').inner_text()
    log_event("Payment Method Selection", {"method": payment_method, "timestamp": datetime.now()})

@pytest.mark.parametrize('payment_method', [
    ('unsupported_method'),
])
def test_unsupported_payment_method(navigate_to_checkout, payment_method):
    """Test behavior when an unsupported payment method is selected."""
    page = navigate_to_checkout
    with pytest.raises(Exception):
        page.click(f'button[aria-label="{payment_method.replace("_", " ").title()}"]')

@pytest.mark.parametrize('payment_method, amount', [
    ('credit_card', 100),
])
def test_ui_element_presence_on_payment(navigate_to_checkout, payment_method, amount):
    """Test positive and negative UI element presence for payment success and error messages."""
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')

    # Positive test: success message
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()

    # Negative test: error message should not be visible
    assert not page.locator('.error-message').is_visible()

    log_event("UI Element Presence Test", {"method": payment_method, "amount": amount, "timestamp": datetime.now()})
