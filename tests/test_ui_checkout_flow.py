import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class TestUICheckoutFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:8000"  # Change to your app URL

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def fill_payment_form(self, card_number, expiry, cvv, amount):
        driver = self.driver
        card_number_input = driver.find_element(By.ID, "cardNumber")
        card_number_input.clear()
        card_number_input.send_keys(card_number)

        expiry_input = driver.find_element(By.ID, "expiryDate")
        expiry_input.clear()
        expiry_input.send_keys(expiry)

        cvv_input = driver.find_element(By.ID, "cvv")
        cvv_input.clear()
        cvv_input.send_keys(cvv)

        amount_input = driver.find_element(By.ID, "amount")
        amount_input.clear()
        amount_input.send_keys(amount)

    def test_ui_post_checkout_success(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        start_time = time.time()

        self.fill_payment_form("4111111111111111", "12/25", "123", "100")

        pay_button = driver.find_element(By.ID, "payButton")
        pay_button.click()

        # Wait for confirmation message
        time.sleep(3)  # Ideally use explicit waits

        confirmation_message = driver.find_element(By.ID, "confirmationMessage")
        self.assertTrue(confirmation_message.is_displayed())
        self.assertIn("Payment successful", confirmation_message.text)

        transaction_status = driver.find_element(By.ID, "transactionStatus")
        self.assertEqual(transaction_status.text, "Success")

        duration = time.time() - start_time
        print(f"Checkout completion time: {duration:.2f} seconds")

    def test_ui_post_checkout_failure(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        self.fill_payment_form("4000000000000000", "12/25", "123", "100")  # Invalid card number to simulate failure

        pay_button = driver.find_element(By.ID, "payButton")
        pay_button.click()

        time.sleep(3)  # Wait for error message

        error_message = driver.find_element(By.ID, "errorMessage")
        self.assertTrue(error_message.is_displayed())
        self.assertIn("Payment failed", error_message.text)

        transaction_status = driver.find_element(By.ID, "transactionStatus")
        self.assertEqual(transaction_status.text, "Failed")

    def test_ui_abandoned_checkout(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        self.fill_payment_form("4111111111111111", "12/25", "123", "100")

        # Simulate user abandoning checkout by not submitting
        time.sleep(5)  # Wait to simulate delay/abandonment

        # Verify no confirmation or error message displayed
        confirmation_present = len(driver.find_elements(By.ID, "confirmationMessage")) > 0
        error_present = len(driver.find_elements(By.ID, "errorMessage")) > 0
        self.assertFalse(confirmation_present)
        self.assertFalse(error_present)

    def test_ui_repeat_checkout(self):
        driver = self.driver
        for _ in range(2):  # Simulate repeat checkout twice
            driver.get(f"{self.base_url}/checkout")
            self.fill_payment_form("4111111111111111", "12/25", "123", "100")
            pay_button = driver.find_element(By.ID, "payButton")
            pay_button.click()
            time.sleep(3)  # Wait for confirmation
            confirmation_message = driver.find_element(By.ID, "confirmationMessage")
            self.assertTrue(confirmation_message.is_displayed())
            self.assertIn("Payment successful", confirmation_message.text)
            transaction_status = driver.find_element(By.ID, "transactionStatus")
            self.assertEqual(transaction_status.text, "Success")

if __name__ == '__main__':
    unittest.main()
