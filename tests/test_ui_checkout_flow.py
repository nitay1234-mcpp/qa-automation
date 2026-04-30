import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    def test_ui_post_checkout_behavior(self):
        driver = self.driver
        driver.get(f"{self.base_url}/checkout")

        # Simulate filling payment info
        card_number_input = driver.find_element(By.ID, "cardNumber")
        card_number_input.send_keys("4111111111111111")

        expiry_input = driver.find_element(By.ID, "expiryDate")
        expiry_input.send_keys("12/25")

        cvv_input = driver.find_element(By.ID, "cvv")
        cvv_input.send_keys("123")

        amount_input = driver.find_element(By.ID, "amount")
        amount_input.clear()
        amount_input.send_keys("100")

        # Submit payment
        pay_button = driver.find_element(By.ID, "payButton")
        pay_button.click()

        # Wait for confirmation message
        time.sleep(3)  # Ideally use explicit waits

        confirmation_message = driver.find_element(By.ID, "confirmationMessage")
        self.assertTrue(confirmation_message.is_displayed())
        self.assertIn("Payment successful", confirmation_message.text)

        # Check UI state reflects success
        transaction_status = driver.find_element(By.ID, "transactionStatus")
        self.assertEqual(transaction_status.text, "Success")

if __name__ == '__main__':
    unittest.main()
