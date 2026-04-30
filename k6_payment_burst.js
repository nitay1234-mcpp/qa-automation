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

// Utility function to generate log-normal distributed amount
function randomLogNormalAmount(mu, sigma, min, max) {
    // Using Box-Muller transform to generate standard normal variable
    let u1 = 1.0 - Math.random();
    let u2 = 1.0 - Math.random();
    let standardNormal = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    let logNormal = Math.exp(mu + sigma * standardNormal);
    // Clamp the value between min and max
    let clamped = Math.min(Math.max(logNormal, min), max);
    return Math.floor(clamped);
}

// Generate randomized payment data for each request with realistic amount distribution
function generatePaymentData() {
    const currencies = ['USD', 'EUR', 'GBP'];
    const paymentMethods = ['credit_card', 'debit_card', 'paypal'];
    const cardNumbers = {
        credit_card: ['4111111111111111', '5555555555554444'],
        debit_card: ['6011000990139424', '3530111333300000'],
    };

    const paymentMethod = randomChoice(paymentMethods);
    const currency = randomChoice(currencies);

    // Parameters for log-normal distribution
    const mu = 4.0; // Mean of log(amount)
    const sigma = 0.5; // Standard deviation
    const minAmount = 10;
    const maxAmount = 500;

    const amount = randomLogNormalAmount(mu, sigma, minAmount, maxAmount);

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
