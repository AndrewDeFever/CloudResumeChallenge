import os
import json
from unittest.mock import patch, MagicMock
from GeoTracker import lambda_handler

# Set required env vars
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

@patch("GeoTracker.requests.get")
def test_lambda_handler_returns_200(mock_get):
    # Simulate ipinfo.io response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP"
    }
    mock_get.return_value = mock_response

    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }
    mock_context = {}

    response = lambda_handler(mock_event, mock_context)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["geo"]["city"] == "Tulsa"
