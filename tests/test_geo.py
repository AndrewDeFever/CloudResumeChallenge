import os
import pytest
from unittest.mock import patch, MagicMock
from GeoTracker import lambda_handler

# Set required environment variable
os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

@patch("GeoTracker.boto3.resource")
@patch("GeoTracker.requests.get")
def test_lambda_handler_returns_200(mock_requests_get, mock_boto3_resource):
    # Mock the ipinfo.io response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP"
    }
    mock_requests_get.return_value = mock_response

    # Mock the DynamoDB resource and table
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    # Simulate a request event with headers
    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }
    mock_context = {}

    # Call the Lambda function
    response = lambda_handler(mock_event, mock_context)

    # Assert response
    assert response["statusCode"] == 200
    assert "Geo data stored" in response["body"]
