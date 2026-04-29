import { PaymentFlow } from '../src/paymentFlow';
import { expect } from 'chai';

describe('Payment Flow Tests', () => {
    it('should successfully process a valid payment', async () => {
        const result = await PaymentFlow.processPayment({
            amount: 100,
            currency: 'USD',
            cardNumber: '4111111111111111',
            expirationDate: '12/25',
            cvv: '123'
        });
        expect(result.status).to.equal('success');
    });

    it('should fail to process payment with invalid card number', async () => {
        const result = await PaymentFlow.processPayment({
            amount: 100,
            currency: 'USD',
            cardNumber: '1234567890123456',
            expirationDate: '12/25',
            cvv: '123'
        });
        expect(result.status).to.equal('failure');
    });

    it('should fail to process payment with expired card', async () => {
        const result = await PaymentFlow.processPayment({
            amount: 100,
            currency: 'USD',
            cardNumber: '4111111111111111',
            expirationDate: '01/20',
            cvv: '123'
        });
        expect(result.status).to.equal('failure');
    });
});
