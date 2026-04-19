# Test Cases for Expired Cards and Payment Limits

## Expired Cards
1. **Test Case: Payment with Expired Card**  
   - **Description:** Verify that the payment fails when using a card that has expired.  
   - **Expected Result:** Payment is declined with an appropriate error message.

2. **Test Case: Payment with Expired Card Notification**  
   - **Description:** Ensure that users are notified when they attempt to use an expired card.  
   - **Expected Result:** User receives a notification about the expired card.

## Payment Limits
3. **Test Case: Payment Above Limit**  
   - **Description:** Validate that the payment is declined when the amount exceeds the user's payment limit.  
   - **Expected Result:** Payment is declined with an appropriate error message.

4. **Test Case: Payment Below Limit**  
   - **Description:** Ensure that the payment is successful when the amount is within the user's payment limit.  
   - **Expected Result:** Payment is processed successfully.

5. **Test Case: Payment Limit Notification**  
   - **Description:** Check that the user is notified when they attempt to exceed their payment limit.  
   - **Expected Result:** User receives a notification about exceeding the payment limit.
