import unittest
import requests
from openapi_core import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core.wrappers.mock import MockRequest, MockResponse
import yaml

class TestDeletePaymentContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load OpenAPI spec from local file or URL
        with open('specs/payments.yaml', 'r') as spec_file:
            spec_dict = yaml.safe_load(spec_file)
        cls.spec = create_spec(spec_dict)
        cls.request_validator = RequestValidator(cls.spec)
        cls.response_validator = ResponseValidator(cls.spec)

    def validate_request_response(self, payment_id, expected_status_code):
        url = f"http://localhost:8000/payments/{payment_id}"

        # Create a mock request for validation
        mock_request = MockRequest(
            host_url="http://localhost:8000",
            path_url=f"/payments/{payment_id}",
            method="DELETE",
            parameters={"path": {"id": payment_id}},
            body=None,
            mimetype=None
        )

        # Send actual DELETE request to the API
        response = requests.delete(url)

        # Create a mock response for validation
        mock_response = MockResponse(
            data=response.json() if response.content else None,
            status_code=response.status_code,
            mimetype=response.headers.get('Content-Type')
        )

        # Validate request and response against OpenAPI spec
        result_request = self.request_validator.validate(mock_request)
        result_response = self.response_validator.validate(mock_request, mock_response)

        # Assert that request and response are valid
        self.assertFalse(result_request.errors, f"Request validation errors: {result_request.errors}")
        self.assertFalse(result_response.errors, f"Response validation errors: {result_response.errors}")

        # Assert expected status code
        self.assertEqual(response.status_code, expected_status_code, f"Expected HTTP status code {expected_status_code} for payment_id {payment_id}")

        return response

    def test_delete_payment_contract(self):
        payment_id = "12345"  # example payment ID
        response = self.validate_request_response(payment_id, 204)
        self.assertIsNone(response.content or None, "Expected empty response body for successful deletion")

    def test_delete_non_existent_payment(self):
        non_existent_payment_id = "nonexistent12345"
        response = self.validate_request_response(non_existent_payment_id, 404)

    def test_delete_invalid_payment_id_format(self):
        invalid_payment_id = "invalid-id!@#"
        response = self.validate_request_response(invalid_payment_id, 400)

    def test_delete_unauthorized_access(self):
        # Here we simulate unauthorized by not sending auth headers or sending invalid token
        payment_id = "12345"
        url = f"http://localhost:8000/payments/{payment_id}"

        mock_request = MockRequest(
            host_url="http://localhost:8000",
            path_url=f"/payments/{payment_id}",
            method="DELETE",
            parameters={"path": {"id": payment_id}},
            body=None,
            mimetype=None
        )

        # Send request without authorization headers
        response = requests.delete(url, headers={})

        mock_response = MockResponse(
            data=response.json() if response.content else None,
            status_code=response.status_code,
            mimetype=response.headers.get('Content-Type')
        )

        result_request = self.request_validator.validate(mock_request)
        result_response = self.response_validator.validate(mock_request, mock_response)

        self.assertFalse(result_request.errors, f"Request validation errors: {result_request.errors}")
        self.assertFalse(result_response.errors, f"Response validation errors: {result_response.errors}")
        self.assertIn(response.status_code, [401, 403], "Expected HTTP status code 401 or 403 for unauthorized access")

if __name__ == '__main__':
    unittest.main()
