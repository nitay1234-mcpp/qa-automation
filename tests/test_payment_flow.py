import pytest
from playwright.sync_api import Page


def test_successful_payment(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()


def test_payment_with_invalid_amount(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '-50')  # Invalid amount
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_zero_amount(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '0')  # Zero amount
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_large_amount(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '1000000')  # Large amount
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_missing_amount(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '')  # Missing amount
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_credit_card(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4111111111111111')  # Valid credit card
    page.fill('[aria-label="Expiry date"]', '12/25')
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()


def test_payment_with_network_failure(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    # Simulate network failure
    page.route('**/*', lambda route: route.abort())
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_fraud_detection(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4000000000000002')  # Known fraud card
    page.click('button[type="submit"]')
    page.wait_for_selector('.fraud-detection-message')
    assert page.locator('.fraud-detection-message').is_visible()  # Check for fraud detection message


def test_payment_with_expired_card(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4111111111111111')  # Valid card
    page.fill('[aria-label="Expiry date"]', '01/20')  # Expired card
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_invalid_card_number(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '1234567890123456')  # Invalid card number
    page.fill('[aria-label="Expiry date"]', '12/25')
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_incorrect_cvv(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4111111111111111')  # Valid card
    page.fill('[aria-label="Expiry date"]', '12/25')
    page.fill('[aria-label="CVV"]', '999')  # Incorrect CVV
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_different_currency(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Currency"]', 'EUR')  # Different currency
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_missing_card_details(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.click('button[type="submit"]')  # Missing card details
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for error message


def test_payment_with_payment_method_switching(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4111111111111111')
    # Simulate switching to PayPal
    page.click('[aria-label="Switch to PayPal"]')
    page.fill('[aria-label="PayPal email"]', 'user@example.com')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()


def test_payment_with_promotional_code(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Promotional code"]', 'SUMMER21')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()  # Ensure payment is successful with discount


def test_payment_timeout(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    # Simulate timeout
    page.route('**/*', lambda route: route.abort())
    page.click('button[type="submit"]')
    page.wait_for_selector('.error-message')
    assert page.locator('.error-message').is_visible()  # Check for timeout error message


def test_payment_with_saved_payment_method(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Saved payment method"]', 'user@example.com')  # Use saved method
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()  # Check for successful payment


def test_payment_with_special_characters_in_name(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', '100')
    page.fill('[aria-label="Card number"]', '4111111111111111')  # Valid card
    page.fill('[aria-label="Cardholder name"]', 'O'Neill')  # Special character
    page.fill('[aria-label="Expiry date"]', '12/25')
    page.fill('[aria-label="CVV"]', '123')
    page.click('button[type="submit"]')
    page.wait_for_selector('.payment-success')
    assert page.locator('.payment-success').is_visible()  # Check for successful payment
