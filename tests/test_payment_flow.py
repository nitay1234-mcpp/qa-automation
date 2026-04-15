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
