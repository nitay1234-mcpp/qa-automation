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


# New test cases added for enhanced coverage

# Test other payment methods (e.g., bank transfer, digital wallet)
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

# Test complete checkout flow including cart validation and address input
@pytest.mark.parametrize('cart_valid, address_valid, expected_error', [
    (True, True, None),
    (False, True, 'Invalid cart'),
    (True, False, 'Invalid address'),
])
def test_complete_checkout_flow(page: Page, cart_valid, address_valid, expected_error):
    page.goto('https://staging.novapay.io/cart')
    if not cart_valid:
        page.evaluate('window.cartIsValid = false')
    if not address_valid:
        page.fill('[aria-label="Shipping address"]', '')
    else:
        page.fill('[aria-label="Shipping address"]', '123 Test St')
    page.click('button[aria-label="Proceed to checkout"]')
    if expected_error:
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        assert expected_error in page.locator('.error-message').inner_text()
        log_event("Checkout Flow Error", {"error": expected_error, "timestamp": datetime.now()})
    else:
        page.wait_for_selector('.checkout-page')
        assert page.url.endswith('/checkout')
        log_event("Checkout Flow Success", {"timestamp": datetime.now()})

# Security test for fraudulent payment detection
@pytest.mark.parametrize('payment_details, expected_error', [
    ({'card_number': '4111111111111111', 'cvv': '123', 'fraud_flag': True}, 'Fraudulent payment detected'),
    ({'card_number': '4111111111111111', 'cvv': '123', 'fraud_flag': False}, None),
])
def test_fraudulent_payment_detection(navigate_to_checkout, payment_details, expected_error):
    page = navigate_to_checkout
    page.fill('[aria-label="Card Number"]', payment_details['card_number'])
    page.fill('[aria-label="CVV"]', payment_details['cvv'])
    if payment_details['fraud_flag']:
        page.evaluate('window.fraudFlag = true')
    page.click('button[type="submit"]')
    if expected_error:
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        assert expected_error in page.locator('.error-message').inner_text()
        log_event("Fraud Detection", {"error": expected_error, "timestamp": datetime.now()})
    else:
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
        log_event("Payment Success", {"timestamp": datetime.now()})

# New test case for timeout during payment processing
@pytest.mark.parametrize('amount, expected_error', [
    (100, 'Payment processing timeout'),
])
def test_payment_processing_timeout(navigate_to_checkout, amount, expected_error):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', str(amount))
    # Simulate timeout by delaying response or interaction
    page.evaluate("window.simulateTimeout = true;")
    page.click('button[type="submit"]')

    # Check for timeout error message
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()
    assert expected_error in page.locator('.error-message').inner_text()
    log_event("Payment Timeout", {"amount": amount, "error": expected_error, "timestamp": datetime.now()})

# New test case for concurrency issues when multiple payments processed simultaneously
def perform_payment(page: Page, amount: float):
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Concurrent Payment Success", {"amount": amount, "timestamp": datetime.now()})

@pytest.mark.parametrize('amounts', [
    ([100, 200, 300]),  # Simultaneous payments
])
def test_concurrency_payments(page: Page, amounts):
    page.goto('https://staging.novapay.io/checkout')
    threads = []
    for amount in amounts:
        t = threading.Thread(target=perform_payment, args=(page, amount))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Additional test cases for enhanced coverage

# 1. Additional payment methods (apple pay, google pay)
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

# 2. Payment in different currencies/localization
@pytest.mark.parametrize('currency, amount, expected_success', [
    ('USD', 100, True),
    ('EUR', 85, True),
    ('JPY', 11000, True),
])
def test_payment_in_different_currencies(navigate_to_checkout, currency, amount, expected_success):
    page = navigate_to_checkout
    page.select_option('select[aria-label="Currency"]', currency)
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    if expected_success:
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
        log_event("Payment Success", {"currency": currency, "amount": amount, "timestamp": datetime.now()})

# 3. Partial and split payments - enhanced edge cases
@pytest.mark.parametrize('partial_amounts, expected_error', [
    ([0, 100], 'Invalid partial payment amount'),  # Zero amount in split
    ([50, -10], 'Invalid partial payment amount'),  # Negative amount in split
    ([50, 51], 'Total exceeds original amount'),  # Sum exceeds original
    ([50, 50], None),  # Valid split
    ([100], None),  # Single payment equal to total
])
def test_partial_and_split_payments_edge_cases(navigate_to_checkout, partial_amounts, expected_error):
    page = navigate_to_checkout
    original_total = sum(partial_amounts)
    page.fill('[aria-label="Payment amount"]', str(original_total))
    for i, amt in enumerate(partial_amounts):
        if i > 0:
            page.click('button[aria-label="Add payment method"]')
        page.fill(f'[aria-label="Split payment amount {i+1}"]', str(amt))
    page.click('button[type="submit"]')

    if expected_error:
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        assert expected_error in page.locator('.error-message').inner_text()
        log_event("Partial/Split Payment Error", {"amounts": partial_amounts, "error": expected_error, "timestamp": datetime.now()})
    else:
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
        log_event("Partial/Split Payment Success", {"amounts": partial_amounts, "timestamp": datetime.now()})

# 4. Payment access by user roles
@pytest.mark.parametrize('user_role, expected_access', [
    ('admin', True),
    ('user', False),
])
def test_payment_access_by_user_role(navigate_to_checkout, user_role, expected_access):
    page = navigate_to_checkout
    page.evaluate(f'window.setUserRole("{user_role}")')
    page.goto('https://staging.novapay.io/checkout')
    if expected_access:
        assert page.locator('button[type="submit"]').is_enabled()
    else:
        assert page.locator('button[type="submit"]').is_disabled()
    log_event("User Role Access", {"role": user_role, "timestamp": datetime.now()})

# 5. Refunds and chargebacks
# Test the refund and chargeback flow
@pytest.mark.parametrize()
def test_refund_and_chargeback_flow(navigate_to_checkout):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    page.click('button[aria-label="Request refund"]')
    page.fill('[aria-label="Refund amount"]', '50')
    page.click('button[type="submit"]')
    page.wait_for_selector('.refund-success')
    assert page.locator('.refund-success').is_visible()
    log_event("Refund Processed", {"timestamp": datetime.now()})

# 6. Accessibility checks
# Ensure accessibility of the payment form
@pytest.mark.parametrize()
def test_accessibility_of_payment_form(navigate_to_checkout):
    page = navigate_to_checkout
    assert page.locator('form[aria-label="Payment form"]').is_visible()
    inputs = page.locator('form[aria-label="Payment form"] input')
    for i in range(inputs.count()):
        assert inputs.nth(i).get_attribute('aria-label') is not None
    log_event("Accessibility Check", {"timestamp": datetime.now()})

# 7. Retry mechanism
# Test the retry mechanism for failed payments
@pytest.mark.parametrize()
def test_retry_payment_mechanism(navigate_to_checkout):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', '100')
    page.evaluate('window.failNextPayment = true')
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    page.click('button[aria-label="Retry"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Payment Retry Success", {"timestamp": datetime.now()})

# 8. Integration with payment gateways
# Test integration with external payment gateways
@pytest.mark.parametrize()
def test_integration_with_gateway(navigate_to_checkout):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.evaluate('window.simulateGatewayCallback(true)')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Gateway Integration Success", {"timestamp": datetime.now()})

# 9. Enhanced concurrency with errors
# Test concurrency with some payments failing
@pytest.mark.parametrize()
def test_concurrency_with_errors(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    results = []
    def perform_payment(amount, should_fail=False):
        page.fill('[aria-label="Payment amount"]', str(amount))
        if should_fail:
            page.evaluate('window.failNextPayment = true')
        page.click('button[type="submit"]')
        try:
            page.wait_for_selector('.payment-success', timeout=5000)
            results.append((amount, True))
            log_event("Concurrent Payment Success", {"amount": amount, "timestamp": datetime.now()})
        except:
            results.append((amount, False))
            log_event("Concurrent Payment Failure", {"amount": amount, "timestamp": datetime.now()})

    import threading
    threads = []
    payments = [(100, False), (200, True), (300, False)]
    for amount, fail in payments:
        t = threading.Thread(target=perform_payment, args=(amount, fail))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    assert any(success for _, success in results), "At least one payment should succeed"

# 10. Basic performance measurement
# Measure basic performance of payment processing
@pytest.mark.parametrize()
def test_basic_performance_measurement(navigate_to_checkout):
    import time
    page = navigate_to_checkout
    start_time = time.time()
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 5, f"Payment processing took too long: {duration} seconds"
    log_event("Performance Test", {"duration": duration, "timestamp": datetime.now()})


# --- New Enhancements Added Below ---

# Cross-Browser Compatibility Test
@pytest.mark.parametrize('browser_name', ['chromium', 'firefox', 'webkit'])
def test_cross_browser_payment_flow(page_factory, browser_name):
    browser = page_factory.launch_browser(browser_name)
    page = browser.new_page()
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    browser.close()

# Mobile Responsiveness Test
@pytest.mark.parametrize('viewport', [
    {'width': 375, 'height': 667},  # iPhone 6/7/8
    {'width': 414, 'height': 736},  # iPhone 6/7/8 Plus
    {'width': 360, 'height': 640},  # Android
])
def test_mobile_responsiveness(page, viewport):
    page.set_viewport_size(viewport)
    page.goto('https://staging.novapay.io/checkout')
    assert page.locator('form[aria-label="Payment form"]').is_visible()

# Session Timeout Handling
def test_session_timeout_handling(navigate_to_checkout):
    page = navigate_to_checkout
    page.evaluate('window.sessionTimeout = true')
    page.wait_for_timeout(3000)  # Wait for session timeout
    page.click('button[type="submit"]')
    page.wait_for_selector('.session-timeout-message')
    assert page.locator('.session-timeout-message').is_visible()
    log_event("Session Timeout", {"timestamp": datetime.now()})

# Payment Method Failover
def test_payment_method_failover(navigate_to_checkout):
    page = navigate_to_checkout
    page.click('button[aria-label="Primary Payment Method"]')
    page.evaluate('window.failPrimaryMethod = true')
    page.click('button[type="submit"]')
    page.wait_for_selector('.failover-payment-option')
    page.click('button[aria-label="Failover Payment Method"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Payment Method Failover", {"timestamp": datetime.now()})

# Currency Conversion Accuracy
@pytest.mark.parametrize('currency, amount, expected_amount', [
    ('USD', 100, 100),
    ('EUR', 85, 100),  # Assuming conversion rate
    ('JPY', 11000, 100),
])
def test_currency_conversion_accuracy(navigate_to_checkout, currency, amount, expected_amount):
    page = navigate_to_checkout
    page.select_option('select[aria-label="Currency"]', currency)
    page.fill('[aria-label="Payment amount"]', str(amount))
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    converted_amount = page.evaluate('window.convertedAmount')
    assert converted_amount == expected_amount
    log_event("Currency Conversion", {"currency": currency, "amount": amount, "converted": converted_amount, "timestamp": datetime.now()})

# Retry Limit and Backoff
@pytest.mark.parametrize('failures_before_success', [0, 1, 3])
def test_retry_limit_and_backoff(navigate_to_checkout, failures_before_success):
    page = navigate_to_checkout
    page.evaluate(f'window.failuresBeforeSuccess = {failures_before_success}')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    if failures_before_success > 0:
        page.wait_for_selector('.error-message')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()
    log_event("Retry Mechanism", {"failures_before_success": failures_before_success, "timestamp": datetime.now()})

# Detailed Fraud Detection Patterns
@pytest.mark.parametrize('pattern', [
    'velocity',  # Multiple payments in short time
    'ip_geolocation_mismatch',
    'blacklisted_card',
])
def test_detailed_fraud_detection_patterns(navigate_to_checkout, pattern):
    page = navigate_to_checkout
    page.evaluate(f'window.fraudPattern = "{pattern}"')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    if pattern == 'velocity':
        for _ in range(5):
            page.click('button[type="submit"]')
    page.wait_for_selector('.fraud-alert')
    assert page.locator('.fraud-alert').is_visible()
    log_event("Fraud Pattern Detected", {"pattern": pattern, "timestamp": datetime.now()})

# Notification and Alert Systems
@pytest.mark.parametrize('notification_type', ['email', 'sms', 'push'])
def test_notification_systems(navigate_to_checkout, notification_type):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.evaluate(f'window.triggerNotification("{notification_type}")')
    page.wait_for_selector(f'.notification-{notification_type}')
    assert page.locator(f'.notification-{notification_type}').is_visible()
    log_event("Notification Sent", {"type": notification_type, "timestamp": datetime.now()})

# Audit Trail and Logging
def test_audit_trail_logging(navigate_to_checkout):
    page = navigate_to_checkout
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    audit_log = page.evaluate('window.getAuditLog()')
    assert 'payment_initiated' in audit_log
    assert 'payment_completed' in audit_log
    log_event("Audit Trail Verified", {"timestamp": datetime.now()})

# Payment Method Expiry
@pytest.mark.parametrize('expired_card', [True, False])
def test_payment_method_expiry(navigate_to_checkout, expired_card):
    page = navigate_to_checkout
    if expired_card:
        page.evaluate('window.cardExpired = true')
    page.fill('[aria-label="Card Number"]', '4111111111111111')
    page.click('button[type="submit"]')
    if expired_card:
        page.wait_for_selector('.card-expiry-error')
        assert page.locator('.card-expiry-error').is_visible()
    else:
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
    log_event("Card Expiry Check", {"expired": expired_card, "timestamp": datetime.now()})

# User Data Privacy
def test_user_data_privacy(navigate_to_checkout):
    page = navigate_to_checkout
    page.fill('[aria-label="Card Number"]', '4111111111111111')
    page.fill('[aria-label="CVV"]', '123')
    logs = page.evaluate('window.getLogs()')
    assert '4111111111111111' not in logs
    assert '123' not in logs
    log_event("User Data Privacy Verified", {"timestamp": datetime.now()})

# Load and Stress Testing
@pytest.mark.parametrize('concurrent_users', [10, 50, 100])
def test_load_and_stress(navigate_to_checkout, concurrent_users):
    page = navigate_to_checkout
    threads = []
    def perform_load_payment():
        page.fill('[aria-label="Payment amount"]', '100')
        page.click('button[type="submit"]')
        page.wait_for_selector('.payment-success')
        assert page.locator('.payment-success').is_visible()
    for _ in range(concurrent_users):
        t = threading.Thread(target=perform_load_payment)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    log_event("Load Test Completed", {"users": concurrent_users, "timestamp": datetime.now()})

# Third-Party Payment Gateway Downtime
def test_gateway_downtime_handling(navigate_to_checkout):
    page = navigate_to_checkout
    page.evaluate('window.gatewayDown = true')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.wait_for_selector('.gateway-error')
    assert page.locator('.gateway-error').is_visible()
    log_event("Gateway Downtime", {"timestamp": datetime.now()})

# Localization and Internationalization
@pytest.mark.parametrize('language', ['en', 'es', 'fr'])
def test_localization_and_internationalization(navigate_to_checkout, language):
    page = navigate_to_checkout
    page.evaluate(f'window.setLanguage("{language}")')
    page.goto('https://staging.novapay.io/checkout')
    assert page.locator('form[aria-label="Payment form"]').is_visible()
    log_event("Localization Test", {"language": language, "timestamp": datetime.now()})

