# Payment Processing - Multi-Currency Support Test Cases

## Test Case 1: Process payment with supported currency (USD)
- **Steps:**
  1. Prepare payment request with amount=100 and currency=USD
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 100
  - Currency: USD
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Payment is processed successfully
  - Response contains currency code USD

## Test Case 2: Process payment with supported currency (EUR)
- **Steps:**
  1. Prepare payment request with amount=100 and currency=EUR
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 100
  - Currency: EUR
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Payment is processed successfully
  - Response contains currency code EUR
  - Conversion rate applied correctly if applicable

## Test Case 3: Process payment with unsupported currency (XYZ)
- **Steps:**
  1. Prepare payment request with amount=100 and currency=XYZ
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 100
  - Currency: XYZ (unsupported currency code)
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Payment is rejected with error message "Unsupported currency"

## Test Case 4: Process payment with currency conversion
- **Steps:**
  1. Prepare payment request with amount=100 USD and currency=EUR (conversion required)
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 100
  - Currency: EUR
  - Base currency: USD
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Conversion rate applied correctly
  - Payment is processed successfully in the target currency

## Test Case 5: Process payment with zero or negative amount
- **Steps:**
  1. Prepare payment request with amount=0 or negative value and currency=USD
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 0 or -100
  - Currency: USD
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Payment is rejected with error message "Invalid amount"

## Test Case 6: Verify currency code format validation
- **Steps:**
  1. Prepare payment request with lowercase currency code (e.g., usd)
  2. Provide valid card details
  3. Submit payment request
- **Test Data:**
  - Amount: 100
  - Currency: usd (lowercase)
  - Card details: valid test card number, CVV, expiry
- **Expected Results:**
  - Payment is either rejected due to invalid currency code format or currency code is normalized to uppercase and accepted
