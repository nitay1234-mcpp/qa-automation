import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://localhost:8000"  # Change to your app URL


class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.card_number_input = page.locator("#cardNumber")
        self.expiry_input = page.locator("#expiryDate")
        self.cvv_input = page.locator("#cvv")
        self.amount_input = page.locator("#amount")
        self.pay_button = page.locator("#payButton")
        self.confirmation_message = page.locator("#confirmationMessage")
        self.transaction_status = page.locator("#transactionStatus")

    def goto(self):
        self.page.goto(f"{BASE_URL}/checkout")

    def fill_payment_info(self, card_number, expiry, cvv, amount):
        self.card_number_input.fill(card_number)
        self.expiry_input.fill(expiry)
        self.cvv_input.fill(cvv)
        self.amount_input.fill("")  # clear existing value
        self.amount_input.fill(amount)

    def submit_payment(self):
        self.pay_button.click()

    def wait_for_confirmation(self):
        expect(self.confirmation_message).to_be_visible(timeout=5000)

    def check_confirmation_text(self, expected_text):
        expect(self.confirmation_message).to_contain_text(expected_text)

    def check_transaction_status(self, expected_status):
        expect(self.transaction_status).to_have_text(expected_status)


@pytest.fixture(scope="function")
def page_context(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def test_ui_post_checkout_behavior(page_context):
    page = page_context
    checkout_page = CheckoutPage(page)

    checkout_page.goto()
    checkout_page.fill_payment_info("4111111111111111", "12/25", "123", "100")
    checkout_page.submit_payment()
    checkout_page.wait_for_confirmation()
    checkout_page.check_confirmation_text("Payment successful")
    checkout_page.check_transaction_status("Success")
