import os
import json
from unittest.mock import patch, MagicMock
from GeoTracker import lambda_handler

@patch("GeoTracker.boto3.resource")  # Patch boto3 first
@patch("GeoTracker.requests.get")    # Then requests.get
def test_lambda_handler_returns_200(mock_requests_get, mock_boto3_resource):
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

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

@patch("GeoTracker.boto3.resource")
@patch("GeoTracker.requests.get")
def test_lambda_handler_handles_ipinfo_failure(mock_requests_get, mock_boto3_resource):
    import os
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

    # Simulate requests.get() throwing a connection error
    mock_requests_get.side_effect = Exception("ipinfo.io timeout")

    # Mock DynamoDB (won’t be reached, but still required)
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    # Simulated incoming API Gateway event
    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }
    mock_context = {}

    # Run the Lambda function
    response = lambda_handler(mock_event, mock_context)

    # Assert Lambda returns HTTP 500 and includes the error message
    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Internal Server Error" in body["message"]
    assert "ipinfo.io timeout" in body["error"]


@patch("GeoTracker.boto3.resource")
@patch("GeoTracker.requests.get")
def test_lambda_handler_handles_dynamodb_failure(mock_requests_get, mock_boto3_resource):
    import os
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitors"

    # Mock successful IP geolocation response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP"
    }
    mock_requests_get.return_value = mock_response

    # Mock DynamoDB table and simulate .put_item() raising an exception
    mock_table = MagicMock()
    mock_table.put_item.side_effect = Exception("DynamoDB write error")
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    # Simulated incoming API Gateway event
    mock_event = {
        "headers": {
            "X-Forwarded-For": "123.123.123.123"
        }
    }
    mock_context = {}

    # Run the Lambda function
    response = lambda_handler(mock_event, mock_context)

    # Assert Lambda returns HTTP 500 and includes the DynamoDB error
    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Internal Server Error" in body["message"]
    assert "DynamoDB write error" in body["error"]
