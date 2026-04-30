import http from 'k6/http';
import { check } from 'k6';

// Utility to generate random integer
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Enhanced payment amount generator for test validation
function generateAmount() {
    const rand = Math.random();
    if (rand < 0.7) {
        return randomInt(10, 100);
    } else if (rand < 0.9) {
        return randomInt(101, 300);
    } else {
        return randomInt(301, 1000);
    }
}

export default function () {
    const amount = generateAmount();

    // Validate amount is within expected ranges
    check(amount, {
        'amount is >= 10': (a) => a >= 10,
        'amount is <= 1000': (a) => a <= 1000,
        'amount is not zero or negative': (a) => a > 0,
    });

    // Additional checks can be added here for distribution validation
}
