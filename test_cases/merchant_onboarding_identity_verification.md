# Merchant Onboarding - Identity Verification Test Cases

## Test Case 1: Submit onboarding with valid KYC documents
- **Steps:**
  1. Prepare merchant onboarding request with complete merchant data including valid ID and address proofs
  2. Submit onboarding request
- **Test Data:**
  - Merchant details: name, email, phone, address
  - Valid ID proof document
  - Valid address proof document
- **Expected Results:**
  - KYC verification passes successfully
  - Merchant status is updated to "verified"

## Test Case 2: Submit onboarding with missing KYC documents
- **Steps:**
  1. Prepare merchant onboarding request with missing ID proof
  2. Submit onboarding request
- **Test Data:**
  - Merchant details: name, email, phone, address
  - Missing ID proof document
- **Expected Results:**
  - KYC verification fails
  - Error message indicating missing required document

## Test Case 3: Submit onboarding with invalid document formats
- **Steps:**
  1. Prepare merchant onboarding request with corrupted or unsupported file formats for documents
  2. Submit onboarding request
- **Test Data:**
  - Merchant details: name, email, phone, address
  - Corrupted or unsupported format documents
- **Expected Results:**
  - KYC verification fails
  - Error message indicating invalid document format

## Test Case 4: Submit onboarding with expired documents
- **Steps:**
  1. Prepare merchant onboarding request with expired ID or address proof documents
  2. Submit onboarding request
- **Test Data:**
  - Merchant details: name, email, phone, address
  - Expired ID proof document
  - Expired address proof document
- **Expected Results:**
  - KYC verification fails
  - Error message indicating document expiration

## Test Case 5: Submit onboarding with mismatched identity details
- **Steps:**
  1. Prepare merchant onboarding request where name on ID document does not match application form
  2. Submit onboarding request
- **Test Data:**
  - Merchant details with mismatched name
  - Valid ID and address proofs
- **Expected Results:**
  - KYC verification fails
  - Error message indicating identity mismatch

## Test Case 6: Simulate AML check failure
- **Steps:**
  1. Prepare merchant onboarding request with data flagged by AML system
  2. Submit onboarding request
- **Test Data:**
  - Merchant details flagged by AML
- **Expected Results:**
  - Onboarding is rejected
  - Reason given as "AML compliance failure"
