import pytest
from playwright.sync_api import Page
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.fixture
def navigate_to_checkout(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    return page

# Existing test cases...

# Additional test case for handling multiple payment methods
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

# Additional test case for edge cases of payment amounts
@pytest.mark.parametrize('amount, expected_error', [
    (9999.98, None),  # Just below limit
    (1000000, 'Amount exceeds limit'),  # Exceeds limit
    (None, 'Invalid amount'),  # None amount
])
def test_edge_cases_payment_amount(navigate_to_checkout, amount, expected_error):
    page = navigate_to_checkout
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

# Additional test case for simulating network errors
@pytest.mark.parametrize('amount, expected_error', [
    (100, 'Network error occurred'),  # Simulated network error
])
def test_network_error_handling(navigate_to_checkout, amount, expected_error):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    # Simulate network error
    page.evaluate("navigator.onLine = false;")
    page.click('button[type="submit"]')

    # Check for error message
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Network Error", {"amount": amount, "error": expected_error, "timestamp": datetime.now()})

# Additional test case for user experience during failures
@pytest.mark.parametrize('amount, expected_message', [
    (100, 'Please check your payment details and try again.'),  # User message on failure
])
def test_user_experience_on_failure(navigate_to_checkout, amount, expected_message):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    # Simulate failure
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert page.locator('.error-message').inner_text() == expected_message
    log_event("User Experience Failure", {"amount": amount, "message": expected_message, "timestamp": datetime.now()})

# Visual Regression Test for Error Messages
@pytest.mark.parametrize('amount, expected_error', [
    (-1, 'Invalid amount'),
])
def test_visual_error_messages(navigate_to_checkout, amount, expected_error):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    page.screenshot(path='screenshots/error_message.png')  # Capture error message screenshot

# Visual Regression Test for Success Messages
@pytest.mark.parametrize('amount', [
    (100),  # Valid amount
])
def test_visual_success_message(navigate_to_checkout, amount):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    page.screenshot(path='screenshots/success_message.png')  # Capture success message screenshot

# Visual Regression Test for Button States
@pytest.mark.parametrize('amount', [
    (100),  # Valid amount
])
def test_visual_button_states(navigate_to_checkout, amount):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    button = page.locator('button[type="submit"]')
    button.hover()  # Simulate hover state
    page.screenshot(path='screenshots/button_hover_state.png')  # Capture screenshot
    button.click()
    page.screenshot(path='screenshots/button_disabled_state.png')  # Capture after click

# Visual Regression Test for Form Input Fields
@pytest.mark.parametrize('amount', [
    ('invalid'),  # Invalid input
    (100),  # Valid input
])
def test_visual_form_input_fields(navigate_to_checkout, amount):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.screenshot(path=f'screenshots/form_input_{amount}.png')  # Capture screenshot
