import pytest
from playwright.sync_api import Page
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.mark.parametrize('input_value', [
    "'; DROP TABLE transactions; --",  # Malicious SQL
    "1 OR 1=1",  # Classic SQL injection
])
def test_sql_injection(page: Page, input_value):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', input_value)
    page.click('button[type="submit"]')
    assert page.locator('.error-message').is_visible()

@pytest.mark.parametrize('input_value', [
    "<script>alert('XSS');</script>",  # Malicious script
    "<img src=x onerror=alert('XSS')>",  # Image error injection
])
def test_xss(page: Page, input_value):
    page.goto('https://staging.novapay.io/checkout')
    page.fill('[aria-label="Payment amount"]', input_value)
    page.click('button[type="submit"]')
    assert page.locator('.error-message').is_visible()


def test_rate_limiting(page: Page):
    for _ in range(10):  # Simulating multiple rapid requests
        page.goto('https://staging.novapay.io/checkout')
        page.fill('[aria-label="Payment amount"]', '100')
        page.click('button[type="submit"]')
    assert page.locator('.rate-limit-message').is_visible()


def test_csrf_protection(page: Page):
    page.goto('https://staging.novapay.io/checkout')
    # Attempt to submit a payment from an unauthorized origin
    page.evaluate("window.location.href='https://unauthorized-origin.com';")
    page.click('button[type="submit"]')
    assert page.locator('.error-message').is_visible()