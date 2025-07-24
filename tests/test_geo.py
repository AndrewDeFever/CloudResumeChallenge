import json
from GeoTracker import lambda_handler

def test_lambda_handler_returns_200():
    # Simulate an API Gateway event with dummy data
    event = {
        "requestContext": {
            "identity": {
                "sourceIp": "123.123.123.123"
            }
        }
    }
    context = {}

    response = lambda_handler(event, context)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
