import pytest
import json

from GeoTracker import lambda_handler


def test_lambda_handler_returns_200(monkeypatch):
    """Test successful Lambda execution with valid IP and geo data."""

    def mock_get(url, timeout=3):
        class MockResponse:
            def json(self):
                return {
                    "country": "US",
                    "region": "Oklahoma",
                    "city": "Tulsa",
                    "org": "TestOrg"
                }
        return MockResponse()

    class MockTable:
        def put_item(self, Item):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    class MockDynamo:
        def Table(self, name):
            return MockTable()

    monkeypatch.setattr("GeoTracker.boto3.resource", lambda service: MockDynamo())
    monkeypatch.setattr("GeoTracker.requests.get", mock_get)

    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent"
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    result = lambda_handler(event, {})
    assert result["statusCode"] == 200
    assert "Geo data stored successfully" in result["body"]


def test_lambda_handler_handles_ipinfo_failure(monkeypatch):
    """Test Lambda handles IP geolocation lookup failure."""

    def mock_get(url, timeout=3):
        raise Exception("ipinfo service down")

    class MockTable:
        def put_item(self, Item):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    class MockDynamo:
        def Table(self, name):
            return MockTable()

    monkeypatch.setattr("GeoTracker.boto3.resource", lambda service: MockDynamo())
    monkeypatch.setattr("GeoTracker.requests.get", mock_get)

    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent"
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    result = lambda_handler(event, {})
    assert result["statusCode"] == 500
    assert "Internal Server Error" in result["body"]


def test_lambda_handler_handles_dynamodb_failure(monkeypatch):
    """Test Lambda handles DynamoDB write failure."""

    def mock_get(url, timeout=3):
        class MockResponse:
            def json(self):
                return {
                    "country": "US",
                    "region": "Oklahoma",
                    "city": "Tulsa",
                    "org": "TestOrg"
                }
        return MockResponse()

    class MockTable:
        def put_item(self, Item):
            raise Exception("DynamoDB write error")

    class MockDynamo:
        def Table(self, name):
            return MockTable()

    monkeypatch.setattr("GeoTracker.boto3.resource", lambda service: MockDynamo())
    monkeypatch.setattr("GeoTracker.requests.get", mock_get)

    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent"
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    result = lambda_handler(event, {})
    assert result["statusCode"] == 500
    assert "Internal Server Error" in result["body"]


def test_lambda_handler_skips_unknown_ip():
    """Test Lambda skips DynamoDB write on unknown IP."""
    event = {
        "headers": {
            "user-agent": "TestAgent"
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    result = lambda_handler(event, {})
    assert result["statusCode"] == 400
    assert "IP address could not be resolved" in result["body"]


def test_lambda_handler_cors_preflight():
    """Test Lambda returns 200 on CORS OPTIONS request."""
    event = {
        "requestContext": {
            "http": {
                "method": "OPTIONS"
            }
        }
    }

    result = lambda_handler(event, {})
    assert result["statusCode"] == 200
    assert "CORS preflight success" in result["body"]

    body = json.loads(response["body"])
    assert "Internal Server Error" in body["message"]
    assert "DynamoDB write error" in body["error"]
