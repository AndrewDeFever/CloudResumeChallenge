import json
import os
from unittest.mock import patch, MagicMock
from GeoTracker import lambda_handler


@patch("GeoTracker.boto3.resource")
@patch("GeoTracker.requests.get")
def test_lambda_handler_returns_200(mock_requests_get, mock_boto3_resource):
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitorsByDay"

    # Mock geo lookup
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP"
    }
    mock_requests_get.return_value = mock_response

    # Mock DynamoDB put_item
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    # Event with IP
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
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Geo data stored successfully"
    assert body["geo"]["region"] == "Oklahoma"


def test_lambda_handler_returns_200():
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitorsByDay"

    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent"
        },
        "requestContext": {
            "http": {
                "method": "POST",
                "sourceIp": "8.8.8.8"
            }
        }
    }

    response = lambda_handler(event, None)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert body["message"] in [
        "Geo data stored successfully",
        "Visit already recorded today"
    ]
def test_lambda_handler_cors_preflight():
    mock_event = {
        "requestContext": {
            "http": {
                "method": "OPTIONS"
            }
        }
    }
    mock_context = {}
    response = lambda_handler(mock_event, mock_context)

    assert response["statusCode"] == 200
    assert "CORS preflight success" in json.loads(response["body"])["message"]
