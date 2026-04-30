#!/bin/bash

# Script to run load tests for payment processing using pytest

# Ensure pytest is installed
pip install pytest

# Navigate to the qa-automation repo directory (assumed current directory)
# Run the load throughput test
pytest -k test_load_throughput -v test_payment_processing.py

# Optionally, run all tests including performance and functional
# pytest -v test_payment_processing.py

# Exit with pytest's exit code
exit $?