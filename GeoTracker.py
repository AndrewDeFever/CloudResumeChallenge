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

    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"})
        }

    try:
        # Get DynamoDB table
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

        # Get IP address from requestContext (fallback if header is missing)
        ip = (
            event.get("headers", {}).get("x-forwarded-for") or
            event.get("requestContext", {}).get("http", {}).get("sourceIp") or
            "unknown"
        )

        # Clean up multi-IP case (X-Forwarded-For may return "IP1, IP2")
        ip = ip.split(",")[0].strip()

        # Optional: capture User-Agent
        user_agent = event.get("headers", {}).get("user-agent", "Unknown")

        # Use ipinfo.io to look up geo info
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json")
        geo_data = geo_response.json()

        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")

        # Store in DynamoDB
        table.put_item(Item={
            "ip_address": ip,
            "visit_time": datetime.utcnow().isoformat(),
            "country": country,
            "region": region,
            "city": city,
            "org": org,
            "user_agent": user_agent
        })

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Geo data stored successfully",
                "ip": ip,
                "geo": {
                    "country": country,
                    "region": region,
                    "city": city,
                    "org": org
                }
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
