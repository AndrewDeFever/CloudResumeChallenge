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

    # Handle CORS preflight request
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"})
        }

    try:
        # Set up DynamoDB resource and table
        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["DYNAMO_TABLE_NAME"]
        table = dynamodb.Table(table_name)

        # Extract IP address from headers or request context
        ip = (
            event.get("headers", {}).get("x-forwarded-for") or
            event.get("requestContext", {}).get("http", {}).get("sourceIp") or
            "unknown"
        ).split(",")[0].strip()

        if ip == "unknown":
            print("IP address could not be resolved, skipping write.")
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Could not resolve client IP."})
            }

        # Optional: capture User-Agent
        user_agent = event.get("headers", {}).get("user-agent", "Unknown")

        # Query IP info service
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        geo_data = geo_response.json()

        # Parse relevant fields
        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")

        # Time metadata
        visit_time = datetime.utcnow().isoformat()
        visit_date = datetime.utcnow().strftime('%Y-%m-%d')

        # Build item
        item = {
            "ip_address": ip,
            "visit_date": visit_date,
            "visit_time": visit_time,
            "country": country,
            "region": region,
            "city": city,
            "org": org,
            "user_agent": user_agent
        }

        print("Writing to table:", table_name)
        print("Item being written:", json.dumps(item, indent=2))

        # Write to DynamoDB
        table.put_item(Item=item)

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
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
