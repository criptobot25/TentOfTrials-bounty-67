"""Tests for tools/log_aggregator.py using independent representative fixtures."""
import pytest
from tools.log_aggregator import (
    JSONLogParser,
    TextLogParser,
    NginxLogParser,
    LogAggregator,
)
from tests.fixtures.sample_logs import (
    REPRESENTATIVE_JSON_LOGS,
    REPRESENTATIVE_TEXT_LOGS,
    REPRESENTATIVE_NGINX_LOGS,
    MALFORMED_LOGS,
)


def test_json_log_parser_representative_fixtures():
    parser = JSONLogParser()
    for line in REPRESENTATIVE_JSON_LOGS:
        parsed = parser.parse(line)
        assert parsed is not None
        assert parsed["format"] == "json"
        assert parsed["level"] in ("error", "warn", "info")
        assert parsed["service"] in ("order-service", "payment-gateway", "market-engine")
        assert parsed["message"] != ""
        assert "fields" in parsed


def test_text_log_parser_representative_fixtures():
    parser = TextLogParser()
    for line in REPRESENTATIVE_TEXT_LOGS:
        parsed = parser.parse(line)
        assert parsed is not None
        assert parsed["format"] == "text"
        assert parsed["level"] in ("error", "warn", "info")
        assert parsed["service"] in ("auth-service", "matching-engine", "websocket-gateway")
        assert parsed["timestamp"] is not None


def test_nginx_log_parser_representative_fixtures():
    parser = NginxLogParser()
    # 200 OK -> info
    p200 = parser.parse(REPRESENTATIVE_NGINX_LOGS[0])
    assert p200 is not None
    assert p200["format"] == "nginx"
    assert p200["level"] == "info"
    assert p200["fields"]["status"] == 200

    # 404 -> warn
    p404 = parser.parse(REPRESENTATIVE_NGINX_LOGS[1])
    assert p404 is not None
    assert p404["level"] == "warn"
    assert p404["fields"]["status"] == 404

    # 500 -> error
    p500 = parser.parse(REPRESENTATIVE_NGINX_LOGS[2])
    assert p500 is not None
    assert p500["level"] == "error"
    assert p500["fields"]["status"] == 500


def test_malformed_logs_graceful_handling():
    json_p = JSONLogParser()
    text_p = TextLogParser()
    nginx_p = NginxLogParser()

    for line in MALFORMED_LOGS:
        assert json_p.parse(line) is None or line.strip() == ""
        assert nginx_p.parse(line) is None
        if not line.strip():
            assert text_p.parse(line) is None


def test_log_aggregator_summary_pipeline():
    aggregator = LogAggregator()
    for line in REPRESENTATIVE_JSON_LOGS + REPRESENTATIVE_TEXT_LOGS + REPRESENTATIVE_NGINX_LOGS:
        aggregator._parse_line(line)

    summary = aggregator.get_summary()
    assert summary["total_entries"] == len(REPRESENTATIVE_JSON_LOGS) + len(REPRESENTATIVE_TEXT_LOGS) + len(REPRESENTATIVE_NGINX_LOGS)
    assert summary["error_count"] > 0
    assert summary["warn_count"] > 0
