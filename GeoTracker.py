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
        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["DYNAMO_TABLE_NAME"]
        table = dynamodb.Table(table_name)

        ip = (
            event.get("headers", {}).get("x-forwarded-for") or
            event.get("requestContext", {}).get("http", {}).get("sourceIp") or
            "unknown"
        ).split(",")[0].strip()

        user_agent = event.get("headers", {}).get("user-agent", "Unknown")
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json")
        geo_data = geo_response.json()

        visit_date = datetime.utcnow().strftime('%Y-%m-%d')

        item = {
            "ip_address": ip,
            "visit_date": visit_date,
            "visit_time": datetime.utcnow().isoformat(),
            "country": geo_data.get("country", "Unknown"),
            "region": geo_data.get("region", "Unknown"),
            "city": geo_data.get("city", "Unknown"),
            "org": geo_data.get("org", "Unknown"),
            "user_agent": user_agent
        }

        # DEBUG: Log item and table name
        print("📝 Writing to table:", table_name)
        print("🧾 Item:", json.dumps(item, indent=2))

        # Attempt write
        response = table.put_item(Item=item)

        print("✅ put_item response:", response)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Geo data stored successfully",
                "ip": ip,
                "geo": {
                    "country": item["country"],
                    "region": item["region"],
                    "city": item["city"],
                    "org": item["org"]
                }
            })
        }

    except Exception as e:
        print("❌ Lambda exception:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }

