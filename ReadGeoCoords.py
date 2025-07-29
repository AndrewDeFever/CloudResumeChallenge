import json
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

# Recursively convert Decimals to float or int
def clean_decimals(obj):
    if isinstance(obj, list):
        return [clean_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: clean_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://www.subrealstudios.com",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        # Only return items that have lat/lng (TTL not expired)
        response = table.scan(
            FilterExpression=Attr("latitude").exists() & Attr("longitude").exists()
        )

        items = response.get("Items", [])
        mapped = []

        for item in items:
            try:
                # Ensure no Decimal slips through
                lat = float(item["latitude"])
                lng = float(item["longitude"])

                mapped.append({
                    "lat": lat,
                    "lng": lng,
                    "city": item.get("city", "Unknown"),
                    "org": item.get("org", "Unknown"),
                    "timestamp": item.get("visit_time", "")
                })
            except Exception as parse_err:
                print("Error mapping item:", parse_err)

        cleaned = clean_decimals(mapped)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(cleaned)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
