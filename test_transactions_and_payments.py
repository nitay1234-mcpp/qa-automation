import pytest
from payment_gateway import PaymentProcessor, TransactionManager

class TestTransactionsAndPayments:

    @pytest.fixture
    def processor(self):
        return PaymentProcessor()

    @pytest.fixture
    def transaction_manager(self):
        return TransactionManager()

    # Tests for GET /transactions endpoint
    def test_get_transactions_with_filters(self, transaction_manager):
        filters = {'date_from': '2023-01-01', 'date_to': '2023-12-31', 'status': 'completed'}
        transactions = transaction_manager.get_transactions(filters=filters)
        assert all(t['status'] == 'completed' for t in transactions), "All transactions should have status 'completed'"

    def test_get_transactions_pagination(self, transaction_manager):
        page_1 = transaction_manager.get_transactions(page=1, per_page=5)
        page_2 = transaction_manager.get_transactions(page=2, per_page=5)
        assert page_1 != page_2, "Pagination should return different results for different pages"

    # Tests for DELETE /payments/{id} endpoint
    def test_cancel_payment_valid_id(self, processor):
        valid_payment_id = 'valid-payment-id-123'
        response = processor.cancel_payment(payment_id=valid_payment_id)
        assert response['status'] == 'cancelled', "Payment should be cancelled for valid ID"

    def test_cancel_payment_invalid_id(self, processor):
        invalid_payment_id = 'invalid-id-xyz'
        response = processor.cancel_payment(payment_id=invalid_payment_id)
        assert response['status'] == 'error', "Error status expected for invalid payment ID"

    def test_cancel_payment_non_existent_id(self, processor):
        non_existent_payment_id = 'non-existent-id-456'
        response = processor.cancel_payment(payment_id=non_existent_payment_id)
        assert response['status'] == 'error', "Error status expected for non-existent payment ID"

    # Additional test for POST /payments if needed
    def test_process_payment_with_invalid_card_details(self, processor):
        invalid_card_info = {'number': '1234567890123456', 'cvv': '000'}
        response = processor.process_payment(amount=100, card_info=invalid_card_info)
        assert response['status'] == 'error', "Expected error status for invalid card details"    
