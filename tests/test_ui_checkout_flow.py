import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestUICheckoutFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        if os.getenv('HEADLESS', 'true').lower() == 'true':
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Change to your app URL

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.test_data = {
            'card_number': '4111111111111111',
            'expiry_date': '12/25',
            'cvv': '123',
            'amount': '100'
        }

    def capture_screenshot(self, name):
        try:
            self.driver.save_screenshot(name)
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")

    def fill_payment_info(self, card_number, expiry_date, cvv, amount):
        driver = self.driver
        try:
            card_number_input = driver.find_element(By.ID, "cardNumber")
            card_number_input.clear()
            card_number_input.send_keys(card_number)

            expiry_input = driver.find_element(By.ID, "expiryDate")
            expiry_input.clear()
            expiry_input.send_keys(expiry_date)

            cvv_input = driver.find_element(By.ID, "cvv")
            cvv_input.clear()
            cvv_input.send_keys(cvv)

            amount_input = driver.find_element(By.ID, "amount")
            amount_input.clear()
            amount_input.send_keys(amount)
        except NoSuchElementException as e:
            self.fail(f"Payment input element not found: {e}")

    def test_ui_post_checkout_behavior(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        self.fill_payment_info(**self.test_data)

        try:
            pay_button = driver.find_element(By.ID, "payButton")
            pay_button.click()
        except NoSuchElementException:
            self.capture_screenshot("pay_button_missing.png")
            self.fail("Pay button not found on checkout page")

        try:
            confirmation_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "confirmationMessage"))
            )
            self.assertIn("Payment successful", confirmation_message.text)
        except TimeoutException:
            self.capture_screenshot("confirmation_message_timeout.png")
            self.fail("Confirmation message not displayed after payment")

        try:
            transaction_status = driver.find_element(By.ID, "transactionStatus")
            self.assertEqual(transaction_status.text, "Success")
        except NoSuchElementException:
            self.capture_screenshot("transaction_status_missing.png")
            self.fail("Transaction status element missing on confirmation page")

    def test_ui_checkout_payment_failure(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        # Use invalid card number to simulate failure
        self.fill_payment_info(card_number="0000000000000000", expiry_date=self.test_data['expiry_date'], cvv=self.test_data['cvv'], amount=self.test_data['amount'])

        try:
            pay_button = driver.find_element(By.ID, "payButton")
            pay_button.click()
        except NoSuchElementException:
            self.capture_screenshot("pay_button_missing_failure.png")
            self.fail("Pay button not found on checkout page")

        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            self.assertIn("Payment failed", error_message.text)
        except TimeoutException:
            self.capture_screenshot("error_message_timeout.png")
            self.fail("Error message not displayed after failed payment")

if __name__ == '__main__':
    unittest.main()
