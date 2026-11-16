import json
import os
from unittest.mock import MagicMock, patch

from GeoTracker import lambda_handler


@patch("GeoTracker.dynamodb.put_item")
@patch("GeoTracker.requests.get")
def test_lambda_handler_returns_200(mock_requests_get, mock_put_item):
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitorsByDay"

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP",
        "loc": "36.1540,-95.9928",
    }
    mock_requests_get.return_value = mock_response

    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent",
        },
        "requestContext": {
            "http": {
                "method": "POST",
                "sourceIp": "8.8.8.8",
            }
        },
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Geo data stored successfully"
    assert body["geo"]["region"] == "Oklahoma"

    mock_requests_get.assert_called_once_with(
        "https://ipinfo.io/8.8.8.8/json",
        timeout=5,
    )
    mock_put_item.assert_called_once()


def test_lambda_handler_missing_ip_returns_400():
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitorsByDay"

    event = {
        "headers": {
            "user-agent": "TestAgent",
        },
        "requestContext": {
            "http": {
                "method": "POST",
            }
        },
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["message"] == "IP address could not be resolved, skipping write."


def test_lambda_handler_cors_preflight():
    event = {
        "requestContext": {
            "http": {
                "method": "OPTIONS",
            }
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert "CORS preflight success" in json.loads(response["body"])["message"]
