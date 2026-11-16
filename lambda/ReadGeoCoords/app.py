import decimal
import json
import os

import boto3
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])


def clean_decimals(obj):
    if isinstance(obj, list):
        return [clean_decimals(item) for item in obj]
    if isinstance(obj, dict):
        return {key: clean_decimals(value) for key, value in obj.items()}
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": os.environ["CORS_ORIGIN"],
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "OPTIONS":
        return response(200, {"message": "CORS preflight success"})

    try:
        items = []
        scan_args = {
            "FilterExpression": Attr("latitude").exists() & Attr("longitude").exists()
        }

        while True:
            result = table.scan(**scan_args)
            items.extend(result.get("Items", []))
            last_key = result.get("LastEvaluatedKey")
            if not last_key:
                break
            scan_args["ExclusiveStartKey"] = last_key

        cleaned = clean_decimals(items)
        mapped = [
            {
                "lat": item.get("latitude"),
                "lng": item.get("longitude"),
                "country": item.get("country", "Unknown"),
                "region": item.get("region", "Unknown"),
                "city": item.get("city", "Unknown"),
                "org": item.get("org", "Unknown"),
                "timestamp": item.get("visit_time", ""),
            }
            for item in cleaned
        ]
        return response(200, mapped)

    except Exception as exc:
        print(f"ReadGeoCoords error: {exc}")
        return response(500, {"message": "Internal Server Error"})
