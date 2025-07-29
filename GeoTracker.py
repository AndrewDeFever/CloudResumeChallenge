import json
import boto3
import os
import time
from datetime import datetime, timezone
import requests

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://www.subrealstudios.com",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"})
        }

    ip = (
        event.get("headers", {}).get("x-forwarded-for") or
        event.get("requestContext", {}).get("http", {}).get("sourceIp")
    )
    if not ip:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "IP address could not be resolved, skipping write."})
        }

    ip = ip.split(",")[0].strip()
    user_agent = event.get("headers", {}).get("user-agent", "Unknown")

    try:
        # Geolocation lookup
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        geo_data = geo_response.json()
        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")
        coords = geo_data.get("loc", "0,0").split(",")

        # Visit metadata
        visit_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        visit_time = datetime.now(timezone.utc).isoformat()
        dedupe_key = f"{ip}#{visit_date}"
        expire_time = int(time.time()) + 86400  # TTL: 24h

        item = {
            "ip_date_key": {"S": dedupe_key},
            "ip_address": {"S": ip},
            "visit_date": {"S": visit_date},
            "visit_time": {"S": visit_time},
            "country": {"S": country},
            "region": {"S": region},
            "city": {"S": city},
            "org": {"S": org},
            "user_agent": {"S": user_agent},
            "expire_time": {"N": str(expire_time)},
           
            item["latitude"] = {"N": str(latitude)}
            item["longitude"] = {"N": str(longitude)}
        }

        print("Writing to DynamoDB (deduplicated):", item)

        # Conditional insert to avoid duplicate daily entries
        dynamodb.put_item(
            TableName=os.environ["DYNAMO_TABLE_NAME"],
            Item=item,
            ConditionExpression='attribute_not_exists(ip_date_key)'
        )

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

    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(f"Visitor {ip} already recorded today — skipping.")
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "Visit already recorded today",
                "ip": ip
            })
        }

    except Exception as e:
        print("Error during Lambda execution:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
