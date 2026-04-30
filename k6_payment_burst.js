import http from 'k6/http';
import { check, sleep } from 'k6';

// Load test options with stages and thresholds
export let options = {
    stages: [
        { duration: `${__ENV.RAMP_UP_DURATION || '1m'}`, target: Number(__ENV.TARGET_USERS) || 100 },
        { duration: `${__ENV.SUSTAIN_DURATION || '5m'}`, target: Number(__ENV.TARGET_USERS) || 100 },
        { duration: `${__ENV.RAMP_DOWN_DURATION || '30s'}`, target: 0 },
    ],
    thresholds: {
        'http_req_duration': ['p(95)<500'], // 95% of requests should be below 500ms
        'http_req_failed': ['rate<0.01'], // Less than 1% failed requests
    },
};

// Utility function to generate random integer in range
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Utility function to pick random element from array
function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

// Generate randomized payment data for each request
function generatePaymentData() {
    const currencies = ['USD', 'EUR', 'GBP'];
    const paymentMethods = ['credit_card', 'debit_card', 'paypal'];
    const cardNumbers = {
        credit_card: ['4111111111111111', '5555555555554444'],
        debit_card: ['6011000990139424', '3530111333300000'],
    };

    const paymentMethod = randomChoice(paymentMethods);
    const currency = randomChoice(currencies);
    const amount = randomInt(10, 500); // Random amount between 10 and 500

    let cardNumber = '';
    if (paymentMethod === 'paypal') {
        cardNumber = '';
    } else {
        cardNumber = randomChoice(cardNumbers[paymentMethod]);
    }

    return {
        amount: amount,
        currency: currency,
        paymentMethod: paymentMethod,
        cardNumber: cardNumber,
        expiryDate: '12/25',
        cvv: '123',
    };
}

export default function () {
    const url = __ENV.PAYMENT_ENDPOINT || 'https://actual-testing-endpoint.com/payment';
    const paymentData = generatePaymentData();
    const payload = JSON.stringify(paymentData);

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, payload, params);

    const checks = {
        'is status 200': (r) => r.status === 200,
        'transaction success': (r) => r.json('status') === 'success',
        'no client error': (r) => r.status < 400,
        'no server error': (r) => r.status < 500,
    };

    check(res, checks);

    if (res.status !== 200 || res.json('status') !== 'success') {
        console.error(`Request failed. Status: ${res.status}, Body: ${res.body}`);
    }

    sleep(Number(__ENV.SLEEP_DURATION) || 1);
}
