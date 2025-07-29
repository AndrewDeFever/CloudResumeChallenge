import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://www.subrealstudios.com",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        # Filter only items that include coordinates
        response = table.scan(
            FilterExpression=Attr("latitude").exists() & Attr("longitude").exists()
        )
        items = response.get("Items", [])
        mapped = []

        for item in items:
            try:
                mapped.append({
                    "lat": float(item["latitude"]),
                    "lng": float(item["longitude"]),
                    "city": item.get("city", "Unknown"),
                    "org": item.get("org", "Unknown"),
                    "timestamp": item.get("visit_time", "")
                })
            except Exception as parse_err:
                print("Error mapping item:", parse_err)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(mapped)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
