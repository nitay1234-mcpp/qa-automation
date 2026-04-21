import pytest
from playwright.sync_api import Page
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, details):
    logging.info(f"{event_type}: {details}")

@pytest.mark.parametrize('transaction_id, expected_result', [
    (12345, 'canceled'),  # Valid cancellation
    (67890, 'not_found'),  # Non-existing transaction ID
])
def test_payment_cancellation(page: Page, transaction_id, expected_result):
    page.goto(f'https://staging.novapay.io/cancel/{transaction_id}')
    if expected_result == 'canceled':
        page.click('button[type="confirm"]')
        page.wait_for_selector('.cancellation-success')
        assert page.locator('.cancellation-success').is_visible()
        log_event("Payment Cancellation Success", {"transaction_id": transaction_id})
    else:
        page.wait_for_selector('.error-message')
        assert page.locator('.error-message').is_visible()
        log_event("Cancellation Not Found", {"transaction_id": transaction_id})
