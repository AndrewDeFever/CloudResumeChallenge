import json
from unittest.mock import patch, MagicMock
from GeoTracker import lambda_handler


@patch("GeoTracker.boto3.resource")  # Patch boto3 first
@patch("GeoTracker.requests.get")    # Then requests.get
def test_lambda_handler_returns_200(mock_requests_get, mock_boto3_resource):
    # Mock response from ipinfo.io
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP"
    }
    mock_requests_get.return_value = mock_response

    # Mock DynamoDB table
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    # Create mock event with headers
    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }
    mock_context = {}

    # Call the Lambda function
    response = lambda_handler(mock_event, mock_context)

    # Assertions
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Geo data stored successfully"
    assert body["geo"]["region"] == "Oklahoma"
