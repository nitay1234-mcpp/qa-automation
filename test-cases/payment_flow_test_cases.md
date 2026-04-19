# Payment Flow Test Cases

| ID | Title | Pre-conditions | Test Steps | Expected Results | Actual Results |
|----|-------|----------------|------------|-----------------|----------------|
| TC-001 | Validate Payment with Valid Card | User is logged in and has items in the cart | 1. Navigate to checkout  
2. Enter valid card details  
3. Submit payment | Payment is processed successfully and order confirmation is displayed |  |  
| TC-002 | Validate Payment with Invalid Card | User is logged in and has items in the cart | 1. Navigate to checkout  
2. Enter invalid card details  
3. Submit payment | Error message is displayed indicating payment failure |  |  
| TC-003 | Validate Payment with Expired Card | User is logged in and has items in the cart | 1. Navigate to checkout  
2. Enter expired card details  
3. Submit payment | Error message is displayed indicating card is expired |  |  
| TC-004 | Validate Payment with Insufficient Funds | User is logged in and has items in the cart | 1. Navigate to checkout  
2. Enter card details with insufficient funds  
3. Submit payment | Error message is displayed indicating insufficient funds |  |  
| TC-005 | Validate Payment Flow with Multiple Items | User is logged in with multiple items in the cart | 1. Navigate to checkout  
2. Enter valid card details  
3. Submit payment | Payment is processed successfully for multiple items |  |