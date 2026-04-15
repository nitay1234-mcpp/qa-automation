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