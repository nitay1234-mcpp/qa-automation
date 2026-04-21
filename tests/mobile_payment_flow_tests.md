# Mobile Payment Flow Test Cases

## Test Case 1: Document Submission
- **Objective:** Verify that merchants can submit KYB documents via the mobile portal.
- **Steps:**
  1. Navigate to the merchant onboarding portal on a mobile device.
  2. Select the option to submit KYB documents.
  3. Upload various document formats (PDF, JPG, etc.) and sizes.
- **Expected Result:** All document submissions are successful and return confirmation.

## Test Case 2: Automated Verification
- **Objective:** Validate the automated verification process for KYB documents.
- **Steps:**
  1. Submit a valid KYB document and record the submission time.
  2. Monitor the verification status.
- **Expected Result:** The document is verified in less than 1 hour for 80% of cases.

## Test Case 3: Manual Review Queue
- **Objective:** Test the manual review process for edge cases.
- **Steps:**
  1. Submit a document that is likely to be flagged as an edge case.
  2. Check the manual review queue.
- **Expected Result:** The document is queued for manual review with all necessary information available to the reviewer.

## Test Case 4: Email Notification System
- **Objective:** Verify email notifications for approval/rejection of onboarding requests.
- **Steps:**
  1. Complete the onboarding process.
  2. Check the email inbox for notifications.
- **Expected Result:** Email notifications are received promptly with accurate content.

## Test Case 5: Performance Testing
- **Objective:** Ensure the onboarding process meets the 24-hour completion goal.
- **Steps:**
  1. Simulate high volumes of onboarding requests.
  2. Measure response times for each request.
- **Expected Result:** All requests complete within the 24-hour goal.

## Test Case 6: User Experience Testing
- **Objective:** Assess the usability of the mobile onboarding process.
- **Steps:**
  1. Conduct usability tests with real users.
  2. Gather feedback on the onboarding experience.
- **Expected Result:** Users report a positive experience with minimal pain points.