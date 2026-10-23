"""Independent, representative log fixtures for log aggregator test suites.

Hand-written based on real production architectures (NGINX, JSON microservices,
syslog plain text) to prevent false-pass regressions from parser-generated data.
"""

REPRESENTATIVE_JSON_LOGS = [
    # Standard ECS-style JSON log
    '{"@timestamp": "2023-11-14T10:15:30Z", "severity": "error", "logger": "order-service", "msg": "Database connection timeout after 5000ms", "order_id": 9842}',
    # Standard Bunyan/Pino style JSON log
    '{"time": 1699956930000, "level": "warn", "service": "payment-gateway", "message": "Stripe webhook retry attempt 2", "attempt": 2}',
    # Standard Python structlog JSON log
    '{"timestamp": "2023-11-14 10:15:32", "lvl": "info", "app": "market-engine", "event": "Orderbook snapshot published", "depth": 50}',
]

REPRESENTATIVE_TEXT_LOGS = [
    # Standard format: [TIMESTAMP] [LEVEL] [SERVICE] MESSAGE
    "2023-11-14 10:20:00 [ERROR] [auth-service] Failed login attempt for user admin from IP 192.168.1.50",
    # Alternative format with parentheses:
    "2023-11-14 10:20:05 [WARN] (matching-engine) Order queue latency exceeded 150ms",
    # Info line:
    "2023-11-14 10:20:10 [INFO] [websocket-gateway] Client connected: conn_id=89234",
]

REPRESENTATIVE_NGINX_LOGS = [
    # 200 OK request
    '192.168.1.10 - - [14/Nov/2023:10:22:00 +0000] "GET /api/v1/health HTTP/1.1" 200 120 "https://app.tent.io" "Mozilla/5.0"',
    # 404 Not Found
    '10.0.0.5 - - [14/Nov/2023:10:22:05 +0000] "GET /api/v1/unknown-endpoint HTTP/1.1" 404 45 "-" "curl/7.88.1"',
    # 500 Server Error
    '172.16.0.20 - - [14/Nov/2023:10:22:10 +0000] "POST /api/v1/orders HTTP/1.1" 500 542 "https://app.tent.io/trade" "Mozilla/5.0"',
]

MALFORMED_LOGS = [
    "",
    "   ",
    "{invalid json truncated",
    '192.168.1.1 - - [not a valid date] "BROKEN REQUEST"',
]
