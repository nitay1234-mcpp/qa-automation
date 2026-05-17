# Contract Tests for Refund Endpoint

## Test Setup
- **Endpoint**: `POST /refunds`
- **Request Body Schema**:
  ```json
  {
    "transactionId": "string",    // Required: ID of the transaction being refunded
    "amount": "number",           // Required: Amount to refund
    "currency": "string",         // Required: Currency of the refund (e.g., "USD")
    "reason": "string"            // Optional: Reason for the refund
  }
  ```

### Test Cases

#### 1. Test Case: Successful Refund
- **Description**: Verify that a valid refund request is processed successfully.
- **Request**:
  ```json
  {
    "transactionId": "abc123",
    "amount": 50.00,
    "currency": "USD",
    "reason": "Customer requested refund."
  }
  ```
- **Expected Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
  ```json
  {
    "status": "success",
    "message": "Refund processed successfully.",
    "refundId": "refund123"
  }
  ```

#### 2. Test Case: Missing Required Fields
- **Description**: Ensure that the API returns an error when required fields are missing.
- **Request**:
  ```json
  {
    "amount": 50.00,
    "currency": "USD"
  }
  ```
- **Expected Response**:
  - **Status Code**: 400 Bad Request
  - **Response Body**:
  ```json
  {
    "status": "error",
    "message": "Missing required fields: transactionId."
  }
  ```

#### 3. Test Case: Invalid Transaction ID
- **Description**: Validate that the API returns an error for an invalid transaction ID.
- **Request**:
  ```json
  {
    "transactionId": "invalid123",
    "amount": 50.00,
    "currency": "USD"
  }
  ```
- **Expected Response**:
  - **Status Code**: 404 Not Found
  - **Response Body**:
  ```json
  {
    "status": "error",
    "message": "Transaction not found."
  }
  ```

#### 4. Test Case: Amount Exceeds Transaction Total
- **Description**: Ensure that the API rejects refunds that exceed the original transaction amount.
- **Request**:
  ```json
  {
    "transactionId": "abc123",
    "amount": 150.00,
    "currency": "USD"
  }
  ```
- **Expected Response**:
  - **Status Code**: 400 Bad Request
  - **Response Body**:
  ```json
  {
    "status": "error",
    "message": "Refund amount exceeds the original transaction amount."
  }
  ```

#### 5. Test Case: Invalid Currency
- **Description**: Validate that the API returns an error for an unsupported currency.
- **Request**:
  ```json
  {
    "transactionId": "abc123",
    "amount": 50.00,
    "currency": "INVALID"
  }
  ```
- **Expected Response**:
  - **Status Code**: 422 Unprocessable Entity
  - **Response Body**:
  ```json
  {
    "status": "error",
    "message": "Invalid currency."
  }
  ```

#### 6. Test Case: Reason for Refund
- **Description**: Ensure that the API accepts a valid reason for the refund.
- **Request**:
  ```json
  {
    "transactionId": "abc123",
    "amount": 50.00,
    "currency": "USD",
    "reason": "Product defective."
  }
  ```
- **Expected Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
  ```json
  {
    "status": "success",
    "message": "Refund processed successfully.",
    "refundId": "refund123"
  }
  ```
