import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "lambda" / "GeoTracker" / "app.py"
SPEC = importlib.util.spec_from_file_location("crc_geotracker", MODULE_PATH)
GeoTracker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GeoTracker)


def setup_module():
    os.environ["DYNAMO_TABLE_NAME"] = "GeoVisitorsByDay"
    os.environ["CORS_ORIGIN"] = "https://resume.subrealstudios.com"


def test_lambda_handler_stores_geolocated_visit():
    event = {
        "headers": {
            "x-forwarded-for": "8.8.8.8",
            "user-agent": "TestAgent",
        },
        "requestContext": {"http": {"method": "POST"}},
    }

    geo = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP",
        "loc": "36.1540,-95.9928",
    }

    with patch.object(GeoTracker, "lookup_ip", return_value=geo), patch.object(
        GeoTracker.dynamodb, "put_item"
    ) as put_item:
        result = GeoTracker.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert json.loads(result["body"])["message"] == "Geo data stored successfully"
    put_item.assert_called_once()

    item = put_item.call_args.kwargs["Item"]
    assert item["region"]["S"] == "Oklahoma"
    assert item["city"]["S"] == "Tulsa"
    assert item["latitude"]["N"] == "36.154"
    assert item["longitude"]["N"] == "-95.9928"


def test_lambda_handler_returns_200_for_duplicate_visit():
    event = {
        "headers": {"x-forwarded-for": "8.8.8.8"},
        "requestContext": {"http": {"method": "POST"}},
    }

    geo = {
        "country": "US",
        "region": "Oklahoma",
        "city": "Tulsa",
        "org": "Fake ISP",
        "loc": "36.1540,-95.9928",
    }

    error = GeoTracker.dynamodb.exceptions.ConditionalCheckFailedException(
        {"Error": {"Code": "ConditionalCheckFailedException", "Message": "duplicate"}},
        "PutItem",
    )

    with patch.object(GeoTracker, "lookup_ip", return_value=geo), patch.object(
        GeoTracker.dynamodb, "put_item", side_effect=error
    ):
        result = GeoTracker.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert json.loads(result["body"])["message"] == "Visit already recorded today"


def test_lambda_handler_cors_preflight():
    event = {"requestContext": {"http": {"method": "OPTIONS"}}}

    result = GeoTracker.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert result["headers"]["Access-Control-Allow-Origin"] == "https://resume.subrealstudios.com"
    assert "CORS preflight success" in json.loads(result["body"])["message"]


def test_lambda_handler_rejects_missing_ip():
    event = {"headers": {}, "requestContext": {"http": {"method": "POST"}}}

    result = GeoTracker.lambda_handler(event, None)

    assert result["statusCode"] == 400
