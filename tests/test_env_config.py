import os

class TestEnvConfig:
    EXTERNAL_SERVICE_URL = os.getenv('EXTERNAL_SERVICE_URL', 'https://default.external.service/api')
    API_KEY = os.getenv('API_KEY', 'default_api_key')

# Add more centralized environment configurations here as needed
