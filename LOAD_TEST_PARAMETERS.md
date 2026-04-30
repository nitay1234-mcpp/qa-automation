# Load Test Parameters and Performance Expectations

This document provides the load testing parameters and performance expectations extracted from the `k6_payment_burst.js` script.

## Load Test Options (Stages)

- Ramp-up duration: Controlled by environment variable `RAMP_UP_DURATION`, default is 1 minute.
- Target users: Controlled by environment variable `TARGET_USERS`, default is 100 virtual users.
- Sustain duration: Controlled by environment variable `SUSTAIN_DURATION`, default is 5 minutes.
- Ramp-down duration: Controlled by environment variable `RAMP_DOWN_DURATION`, default is 30 seconds.

## Performance Thresholds

- 95th percentile of HTTP request duration should be below 500 milliseconds.
- HTTP request failure rate should be less than 1%.

## Request Pacing

- Sleep duration between requests is controlled by environment variable `SLEEP_DURATION`, defaulting to 1 second.

## Structured Format

```json
{
  "load_test_options": {
    "stages": [
      {
        "duration": "RAMP_UP_DURATION (default: 1m)",
        "target_users": "TARGET_USERS (default: 100)"
      },
      {
        "duration": "SUSTAIN_DURATION (default: 5m)",
        "target_users": "TARGET_USERS (default: 100)"
      },
      {
        "duration": "RAMP_DOWN_DURATION (default: 30s)",
        "target_users": 0
      }
    ]
  },
  "performance_thresholds": {
    "http_req_duration": "95th percentile < 500 ms",
    "http_req_failed_rate": "< 1%"
  },
  "request_pacing": {
    "sleep_duration_between_requests": "SLEEP_DURATION (default: 1 second)"
  }
}
```
