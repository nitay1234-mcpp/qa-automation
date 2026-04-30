# Test Cases for Untested Endpoints

This file contains test cases for previously identified untested endpoints to improve test coverage.

| ID    | Title                                                | Pre-conditions                           | Test Steps                                                                                      | Expected Results                                              |
|-------|------------------------------------------------------|-----------------------------------------|------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| TC-015| Validate Error on Payment Processing with Invalid Card Details | User is logged in and has items in cart | 1. Navigate to checkout <br> 2. Enter invalid card details <br> 3. Submit payment                 | Error message is displayed indicating invalid card details   |
| TC-016| Validate Transaction History Retrieval with Filters  | User is logged in and has transaction history | 1. Navigate to transactions page <br> 2. Apply valid filters (date range, status)               | Transactions list is filtered correctly based on applied filters |
| TC-017| Validate Cancel Payment with Non-existent Payment ID | User is logged in                        | 1. Attempt to cancel a payment using a non-existent payment ID                                  | Error message is displayed indicating invalid payment ID     |
| TC-018| Validate Transaction History Retrieval with Boundary Date Filter | User is logged in and has transaction history | 1. Navigate to transactions page <br> 2. Apply filters with boundary date values (e.g., start and end dates at limits) | Transactions list is filtered correctly including boundary dates |
| TC-019| Validate Cancel Payment with Invalid Payment ID Format | User is logged in                        | 1. Attempt to cancel a payment using an invalid payment ID format (e.g., wrong characters or length) | Error message is displayed indicating invalid payment ID format |
| TC-020| Validate Cancel Payment with Missing Payment ID     | User is logged in                        | 1. Attempt to cancel a payment without providing a payment ID                                  | Error message is displayed indicating missing payment ID     |

---

## Notes
- These test cases target improving coverage for untested endpoints.
- Ensure integration into CI/CD pipeline for regular validation.
