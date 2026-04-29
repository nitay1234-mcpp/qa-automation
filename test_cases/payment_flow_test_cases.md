# Reverted Test Cases for Payment Flow

This file has been reverted due to the identification of flaky tests associated with the payment flow.

- **Test Cases Reverted:**
  - Validate Payment with PayPal
  - Validate Payment with Discount Code
  - Validate Payment with Network Timeout
  - Validate User Notification on Payment Status

# Original Test Cases

| ID    | Title                                          | Pre-conditions                                   | Test Steps                                                                                                          | Expected Results                                        |
|-------|------------------------------------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| TC-006| Validate Payment with PayPal                   | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select PayPal as payment method <br> 3. Complete payment                      | Payment is processed successfully and order confirmation is displayed |
| TC-007| Validate Payment with Discount Code            | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid discount code <br> 3. Submit payment                               | Discount is applied and payment is processed successfully       |
| TC-008| Validate Payment with Network Timeout           | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid card details <br> 3. Simulate network timeout and submit payment   | Error message is displayed indicating network timeout          |
| TC-009| Validate User Notification on Payment Status    | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid card details <br> 3. Submit payment                               | User receives notification of payment success or failure         |
