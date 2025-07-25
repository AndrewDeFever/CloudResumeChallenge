import json
import boto3
import os
from datetime import datetime
import requests

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://www.subrealstudios.com",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Preflight OK"})
        }

    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

        # Get IP address
        ip = event.get("headers", {}).get("X-Forwarded-For", "0.0.0.0").split(",")[0]

        # Get geo info
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json")
        geo_data = geo_resp.json()

        item = {
            "ip_address": ip,
            "visit_time": datetime.utcnow().isoformat(),
            "country": geo_data.get("country", "Unknown"),
            "region": geo_data.get("region", "Unknown"),
            "city": geo_data.get("city", "Unknown"),
            "org": geo_data.get("org", "Unknown")
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Geo data stored successfully", "data": item})
        }

    except Exception as e:
        print(f"GeoTracker ERROR: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
