import os
import json
from GeoTracker import lambda_handler

# Set environment variables for the test
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

def test_lambda_handler_returns_200():
    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }

    mock_context = {}

    response = lambda_handler(mock_event, mock_context)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
