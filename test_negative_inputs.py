import pytest
from payment_gateway import PaymentProcessor

class TestNegativeInputValidation:

    @pytest.mark.parametrize("amount, card_info, expected_status", [
        (None, {'number': '4111111111111111', 'cvv': '123'}, 'error'),  # Missing amount
        (-100, {'number': '4111111111111111', 'cvv': '123'}, 'error'),  # Negative amount
        (100, None, 'error'),  # Missing card info
        (100, {'number': '', 'cvv': '123'}, 'error'),  # Empty card number
        (100, {'number': '4111111111111111', 'cvv': ''}, 'error'),  # Empty CVV
        (100, {'number': '4111111111111111'}, 'error'),  # Missing CVV
        (100, {'number': '4111111111111111', 'cvv': '12'}, 'error'),  # Invalid CVV length
        (100, {'number': '4111A11111111111', 'cvv': '123'}, 'error'),  # Invalid characters in card number
    ])
    def test_invalid_payment_inputs(self, amount, card_info, expected_status):
        processor = PaymentProcessor()
        response = processor.process_payment(amount=amount, card_info=card_info)
        assert response['status'] == expected_status, f"Expected {expected_status} for inputs amount={amount}, card_info={card_info}. Got {response['status']}"

    @pytest.mark.parametrize("payment_id, expected_status", [
        (None, 'error'),  # Missing payment ID
        ('', 'error'),  # Empty payment ID
        ('invalid-id!@#', 'error'),  # Invalid format
        ('nonexistent123', 'error'),  # Non-existent payment ID
    ])
    def test_invalid_payment_deletion(self, payment_id, expected_status):
        processor = PaymentProcessor()
        response = processor.delete_payment(payment_id)
        assert response['status'] == expected_status, f"Expected {expected_status} for delete_payment with payment_id={payment_id}. Got {response['status']}"

    @pytest.mark.parametrize("page, page_size, expected_status", [
        (-1, 10, 'error'),  # Invalid page number
        (1, 0, 'error'),  # Invalid page size
        (1, -5, 'error'),  # Negative page size
        (9999, 10, 'success'),  # Very high page number (may be empty but valid)
    ])
    def test_invalid_transaction_history_pagination(self, page, page_size, expected_status):
        processor = PaymentProcessor()
        response = processor.get_transaction_history(page=page, page_size=page_size)
        assert response['status'] == expected_status, f"Expected {expected_status} for transaction history pagination with page={page}, page_size={page_size}. Got {response['status']}"
