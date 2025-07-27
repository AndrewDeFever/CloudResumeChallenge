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

    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"})
        }

    try:
        # Get table name from environment and init DynamoDB
        table_name = os.environ["DYNAMO_TABLE_NAME"]
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)

        # Get IP from headers or request context
        ip = (
            event.get("headers", {}).get("x-forwarded-for") or
            event.get("requestContext", {}).get("http", {}).get("sourceIp") or
            "unknown"
        )
        ip = ip.split(",")[0].strip()  # Strip extra IPs

        # Capture User-Agent
        user_agent = event.get("headers", {}).get("user-agent", "Unknown")

        # Fetch geo data
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        geo_data = geo_response.json()

        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")

        visit_date = datetime.utcnow().strftime('%Y-%m-%d')
        visit_time = datetime.utcnow().isoformat()

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

        print("Writing to table:", os.environ["DYNAMO_TABLE_NAME"])
        print(json.dumps(item, indent=2))

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
        print("Exception occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
