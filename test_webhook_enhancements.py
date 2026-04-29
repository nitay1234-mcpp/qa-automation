import pytest
import logging
from payment_gateway import PaymentProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestWebhookEnhancements:

    @pytest.mark.parametrize("event_data, expected_notification", [
        ({'event': 'payment_success', 'data': {'amount': 100}}, 'Webhook processed successfully.'),
        ({'event': 'payment_failure', 'data': {'amount': 100}}, 'Payment failed. Please check your details.')
    ])
    def test_user_notifications(self, event_data, expected_notification):
        logger.info(f"Testing user notifications for event: {event_data}")
        processor = PaymentProcessor()
        notification = processor.send_notification(event_data)
        assert notification['message'] == expected_notification, f"Expected notification message: {expected_notification}"

    def test_detailed_logging(self):
        logger.info("Testing detailed logging for webhook events.")
        processor = PaymentProcessor()
        event_data = {'event': 'payment_success', 'data': {'amount': 100}}
        processor.handle_webhook(event_data)
        logs = processor.get_logs()  # Assuming this method retrieves logs
        assert any("Webhook processed successfully" in log for log in logs), "Expected log entry for successful webhook processing"

    def test_configurable_retry_settings(self):
        logger.info("Testing configurable retry settings for webhooks.")
        processor = PaymentProcessor()
        user_settings = {'max_retries': 5, 'retry_interval': 10}
        processor.set_retry_settings(user_settings)
        assert processor.max_retries == 5, "Expected max_retries to be set to 5"
        assert processor.retry_interval == 10, "Expected retry_interval to be set to 10"

    def test_monitoring_dashboard(self):
        logger.info("Testing monitoring dashboard functionality.")
        processor = PaymentProcessor()
        dashboard_data = processor.get_dashboard_data()  # Assuming this method retrieves dashboard data
        assert 'success_rate' in dashboard_data, "Expected success_rate in dashboard data"
        assert isinstance(dashboard_data['event_logs'], list), "Expected event_logs to be a list"
