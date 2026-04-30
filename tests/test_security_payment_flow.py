import pytest
from playwright.sync_api import Page
import logging
from datetime import datetime, timedelta
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.fixture
def navigate_to_checkout(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    return page

# Test case for Data Encryption Validation
@pytest.mark.parametrize('card_number, cvv', [
    ('4111111111111111', '123'),
])
def test_data_encryption_validation(navigate_to_checkout, card_number, cvv):
    page = navigate_to_checkout
    # Fill payment details
    page.fill('[aria-label="Card Number"]', card_number)
    page.fill('[aria-label="CVV"]', cvv)
    # Submit payment
    page.click('button[type="submit"]')

    # Intercept network requests to verify encryption
    requests = []
    def capture_request(route, request):
        requests.append(request)
        route.continue_()

    page.route('**/payment', capture_request)

    # Wait for some time to capture requests
    time.sleep(3)

    # Check intercepted requests for encrypted payload
    encrypted_found = False
    for req in requests:
        if 'card_number' in req.post_data or 'cvv' in req.post_data:
            encrypted_found = False
            break
        else:
            encrypted_found = True

    assert encrypted_found, "Sensitive payment data should be encrypted during transmission"
    log_event("Data Encryption Validation", {"card_number": card_number, "timestamp": datetime.now()})

# Test case for Session Management - expired session
@pytest.mark.parametrize('wait_time_seconds, expected_error', [
    (5, 'Session expired'),  # Simulate session expiration after 5 seconds
])
def test_session_expiration(navigate_to_checkout, wait_time_seconds, expected_error):
    page = navigate_to_checkout
    # Wait to simulate session expiration
    time.sleep(wait_time_seconds)
    # Attempt to submit payment
    page.fill('[aria-label="Card Number"]', '4111111111111111')
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')

    # Expect error message about session expiration
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Session Management", {"error": expected_error, "timestamp": datetime.now()})

# Test case for Injection Attacks - SQL Injection and Script Injection
@pytest.mark.parametrize('input_field, injection_string, expected_error', [
    ('[aria-label="Card Number"]', "' OR '1'='1", 'Invalid input'),  # SQL Injection
    ('[aria-label="Card Number"]', "<script>alert('xss')</script>", 'Invalid input'),  # Script Injection
])
def test_injection_attacks(navigate_to_checkout, input_field, injection_string, expected_error):
    page = navigate_to_checkout
    # Inject malicious input
    page.fill(input_field, injection_string)
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')

    # Expect error message about invalid input
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Injection Attacks", {"input_field": input_field, "injection_string": injection_string, "timestamp": datetime.now()})

