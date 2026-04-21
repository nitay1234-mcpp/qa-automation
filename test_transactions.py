import pytest
from payment_gateway import PaymentProcessor

class TestTransactionHistory:

    def test_retrieve_transaction_history(self):
        processor = PaymentProcessor()
        response = processor.get_transaction_history()
        assert response['status'] == 'success', "Expected 'success' status for retrieving transaction history."
        assert isinstance(response['data'], list), "Expected data to be a list of transactions."

    def test_retrieve_transaction_history_with_pagination(self):
        processor = PaymentProcessor()
        response = processor.get_transaction_history(page=1, page_size=10)
        assert response['status'] == 'success', "Expected 'success' status for paginated transaction history."
        assert len(response['data']) <= 10, "Expected no more than 10 transactions per page."

    def test_retrieve_transaction_history_with_filtering(self):
        processor = PaymentProcessor()
        response = processor.get_transaction_history(filter={'date': '2023-01-01'})
        assert response['status'] == 'success', "Expected 'success' status for filtered transaction history."
        assert all(transaction['date'] == '2023-01-01' for transaction in response['data']), "Expected all transactions to match the filter criteria."
