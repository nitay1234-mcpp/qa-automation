import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 50 }, // Ramp up to 50 users
        { duration: '1m', target: 50 },  // Stay at 50 users
        { duration: '10s', target: 0 },  // Ramp down to 0 users
    ],
};

export default function () {
    let url = 'https://test-api.example.com/payment';
    let payload = JSON.stringify({
        amount: 100,
        currency: 'USD',
        paymentMethod: 'credit_card',
        cardNumber: '4111111111111111',
        cardExpiry: '12/23',
        cardCVC: '123',
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let res = http.post(url, payload, params);

    check(res, {
        'is status 200': (r) => r.status === 200,
        'transaction successful': (r) => r.json('success') === true,
    });

    sleep(1);
}
