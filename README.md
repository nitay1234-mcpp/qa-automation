# qa-automation

## Project Overview
The `qa-automation` project is designed to provide a comprehensive end-to-end testing suite using Playwright and pytest. It aims to ensure the reliability and correctness of payment flows, merchant onboarding processes, and API contract adherence. This automation framework enables efficient testing and validation of critical user journeys.

## Installation Instructions
To set up the project, please follow these steps:
1. Ensure you have Python 3.7 or higher installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/nitay1234-mcpp/qa-automation.git
   ```
3. Navigate to the project directory:
   ```bash
   cd qa-automation
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the test suite, execute the following command:
```bash
pytest tests/
```
This will execute all test cases in the `tests` directory. For more specific tests, you can run:
```bash
pytest tests/test_payment_flow.py
```

## Contributing
We welcome contributions to the `qa-automation` project! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

## Testing Instructions
To execute the full test suite, run:
```bash
pytest
```
For detailed output, use:
```bash
pytest -v
```
The results will indicate passed and failed tests, along with relevant error messages.

## Additional Resources
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [pytest Documentation](https://docs.pytest.org/en/latest/)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact Information
For questions or support, please reach out to [your_email@example.com].