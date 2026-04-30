# Detailed and Stable Test Cases for Payment Flow

This file contains detailed and stable test cases covering supported payment methods, success criteria, error handling, and integration points.

| ID    | Title                                          | Pre-conditions                                   | Test Steps                                                                                                          | Expected Results                                        |
|-------|------------------------------------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| TC-006| Validate Payment with PayPal                   | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select PayPal as payment method <br> 3. Complete payment                      | Payment is processed successfully and order confirmation is displayed |
| TC-007| Validate Payment with Discount Code            | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid discount code <br> 3. Submit payment                               | Discount is applied and payment is processed successfully       |
| TC-008| Validate Payment with Network Timeout           | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid card details <br> 3. Simulate network timeout and submit payment   | Error message is displayed indicating network timeout          |
| TC-009| Validate User Notification on Payment Status    | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Enter valid card details <br> 3. Submit payment                               | User receives notification of payment success or failure         |
| TC-010| Validate Payment with Credit Card               | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select Credit Card as payment method <br> 3. Complete payment                  | Payment is processed successfully and order confirmation is displayed |
| TC-011| Validate Payment Cancellation                    | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select any payment method <br> 3. Cancel payment before completion             | Payment is cancelled and user is returned to the checkout page  |
| TC-012| Validate Payment Failure due to Insufficient Funds | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select payment method <br> 3. Use card or account with insufficient funds      | Payment failure message is displayed and payment is not processed |
| TC-013| Validate Payment Integration with Third-Party Gateway | User is logged in and has items in the cart    | 1. Navigate to checkout  <br> 2. Select payment gateway method <br> 3. Complete payment using third-party gateway | Payment is processed successfully and order confirmation is displayed |
| TC-014| Validate Refund Process                          | User has completed a payment                     | 1. Navigate to order history  <br> 2. Request a refund for a completed order                                    | Refund is processed successfully and status is updated         |
| TC-021| Validate Payment Failure with Card Declined Due to Fraud Detection | User is logged in and has items in the cart | 1. Navigate to checkout <br> 2. Enter card details that trigger fraud detection <br> 3. Submit payment | Payment is declined and user is notified about suspected fraud |
| TC-022| Validate Payment Failure with Expired Card      | User is logged in and has items in the cart    | 1. Navigate to checkout <br> 2. Enter expired card details <br> 3. Submit payment                               | Payment failure message is displayed indicating expired card   |

---

## Notes
- Supported payment methods include PayPal, Credit Card, Discount Codes, and third-party gateways.
- Success criteria include correct processing, confirmation display, and notification to users.
- Error handling covers network timeouts, insufficient funds, payment cancellations, and additional edge cases like fraud detection and expired cards.
- Integration points include third-party payment gateways and refund processing.