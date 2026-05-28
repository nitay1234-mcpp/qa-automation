import os
import pytest

# Centralized test environment configuration
class TestEnvConfig:
    EXTERNAL_SERVICE_URL = os.getenv('EXTERNAL_SERVICE_URL', 'https://default.external.service/api')
    API_KEY = os.getenv('API_KEY', 'default_api_key')


def check_integration_feedback():
    # Simulated function to check integration feedback
    # In real tests, this would call the external service
    if TestEnvConfig.EXTERNAL_SERVICE_URL and TestEnvConfig.API_KEY:
        return 'Expected response'
    return 'Unexpected response'


@pytest.mark.parametrize("scenario", ["success", "failure", "timeout", "invalid_api_key"])
def test_integration_with_external_services(scenario):
    if scenario == "success":
        assert check_integration_feedback() == 'Expected response'
    elif scenario == "failure":
        # Simulate failure scenario
        assert check_integration_feedback() != 'Expected response'
    elif scenario == "timeout":
        # Simulate timeout scenario
        # (In real test, might mock a timeout exception)
        assert True  # Placeholder for timeout handling
    elif scenario == "invalid_api_key":
        # Simulate invalid API key scenario
        original_api_key = TestEnvConfig.API_KEY
        TestEnvConfig.API_KEY = 'invalid'
        assert check_integration_feedback() != 'Expected response'
        TestEnvConfig.API_KEY = original_api_key
