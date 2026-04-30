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

    def test_delete_payment_contract(self):
        payment_id = "12345"  # example payment ID
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

        # Additional assertions for successful scenario
        self.assertEqual(response.status_code, 204, "Expected HTTP status code 204 No Content for successful deletion")
        self.assertIsNone(response.content or None, "Expected empty response body for successful deletion")

if __name__ == '__main__':
    unittest.main()
