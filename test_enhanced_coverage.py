import pytest
from payment_gateway import PaymentProcessor

class TestAuthenticationAuthorization:
    def test_unauthorized_access(self):
        processor = PaymentProcessor(auth_token=None)  # Simulate missing auth token
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert response['status'] == 'unauthorized', "Expected 'unauthorized' status for missing auth token"

    def test_expired_token(self):
        processor = PaymentProcessor(auth_token='expired_token')  # Simulate expired token
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert response['status'] == 'unauthorized', "Expected 'unauthorized' status for expired auth token"

class TestRateLimiting:
    def test_rate_limit_exceeded(self):
        processor = PaymentProcessor()
        for _ in range(100):  # Simulate allowed requests
            processor.process_payment(amount=10, card_info={'number': '4111111111111111', 'cvv': '123'})
        response = processor.process_payment(amount=10, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert response['status'] == 'rate_limited', "Expected 'rate_limited' status after exceeding request limit"

class TestInputValidation:
    def test_invalid_currency_code(self):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, currency='XYZ')
        assert response['status'] == 'error', "Expected 'error' status for invalid currency code"

    def test_invalid_metadata(self):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'}, metadata={'unexpected_field': object()})
        assert response['status'] == 'error', "Expected 'error' status for invalid metadata"

class TestRefundEnhancements:
    def test_partial_refund_combined_payments(self):
        processor = PaymentProcessor()
        # Simulate multiple payments
        processor.process_payment(amount=50, card_info={'number': '4111111111111111', 'cvv': '123'})
        processor.process_payment(amount=30, card_info={'number': '4111111111111111', 'cvv': '123'})
        response = processor.process_refund(amount=60, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert response['status'] == 'success', "Expected 'success' for partial refund across multiple payments"

    def test_refund_reversal(self):
        processor = PaymentProcessor()
        refund_response = processor.process_refund(amount=50, card_info={'number': '4111111111111111', 'cvv': '123'})
        assert refund_response['status'] == 'success'
        reversal_response = processor.reverse_refund(refund_id=refund_response.get('refund_id'))
        assert reversal_response['status'] == 'success', "Expected 'success' for refund reversal"

class TestPaymentMethodUpdates:
    def test_update_saved_payment_method(self):
        processor = PaymentProcessor()
        save_response = processor.save_payment_method({'number': '4111111111111111', 'cvv': '123'})
        assert save_response['status'] == 'saved'
        update_response = processor.update_payment_method(save_response.get('method_id'), {'number': '5500000000000004', 'cvv': '321'})
        assert update_response['status'] == 'updated', "Expected 'updated' status for payment method update"

    def test_delete_saved_payment_method(self):
        processor = PaymentProcessor()
        save_response = processor.save_payment_method({'number': '4111111111111111', 'cvv': '123'})
        assert save_response['status'] == 'saved'
        delete_response = processor.delete_payment_method(save_response.get('method_id'))
        assert delete_response['status'] == 'deleted', "Expected 'deleted' status for payment method deletion"

class TestTransactionExportReporting:
    def test_export_transactions(self):
        processor = PaymentProcessor()
        response = processor.export_transactions(format='csv')
        assert response['status'] == 'success'
        assert 'csv_data' in response, "Expected CSV data in export response"

class TestFailureRecoveryRollbacks:
    def test_payment_failure_rollback(self):
        processor = PaymentProcessor()
        # Simulate failure during payment processing
        response = processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123', 'simulate_failure': True})
        assert response['status'] == 'error'
        rollback_response = processor.rollback_transaction(transaction_id=response.get('transaction_id'))
        assert rollback_response['status'] == 'rolled_back', "Expected 'rolled_back' status for failed payment rollback"

class TestWebhookEventVariability:
    def test_malformed_payload(self):
        processor = PaymentProcessor()
        response = processor.handle_webhook({'malformed': True})
        assert response['status'] == 'error', "Expected 'error' status for malformed webhook payload"

    def test_delayed_event(self):
        processor = PaymentProcessor()
        response = processor.handle_webhook({'event': 'payment_success', 'delay': True})
        assert response['status'] == 'processed', "Expected 'processed' status for delayed webhook event"

    def test_duplicate_event(self):
        processor = PaymentProcessor()
        event_data = {'event': 'payment_success', 'data': {'amount': 100}}
        processor.handle_webhook(event_data)
        response = processor.handle_webhook(event_data)  # Duplicate
        assert response['status'] == 'duplicate', "Expected 'duplicate' status for repeated webhook event"

class TestUserExperienceEnhancements:
    def test_error_message_display(self):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=-100, card_info={'number': '4111111111111111', 'cvv': '123'})
        ui_state = processor.get_ui_state(response.get('transaction_id'))
        assert ui_state['error_message'] is not None, "Expected error message display for failed payment"

    def test_loading_state(self):
        processor = PaymentProcessor()
        processor.start_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        ui_state = processor.get_ui_state()
        assert ui_state['loading'], "Expected loading state during payment processing"

class TestLoggingMonitoringDepth:
    def test_critical_event_logging(self):
        processor = PaymentProcessor()
        processor.process_payment(amount=100, card_info={'number': '4111111111111111', 'cvv': '123'})
        logs = processor.get_logs()
        assert any('payment processed' in log.lower() for log in logs), "Expected critical payment processed event in logs"

    def test_error_condition_logging(self):
        processor = PaymentProcessor()
        processor.process_payment(amount=-100, card_info={'number': '4111111111111111', 'cvv': '123'})
        logs = processor.get_logs()
        assert any('error' in log.lower() for log in logs), "Expected error condition logged"