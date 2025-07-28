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

    # CORS preflight check
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"})
        }

    # Extract IP
    ip = (
        event.get("headers", {}).get("x-forwarded-for") or
        event.get("requestContext", {}).get("http", {}).get("sourceIp")
    )

    if not ip:
        print("No IP address found.")
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "IP address could not be resolved, skipping write."})
        }

    ip = ip.split(",")[0].strip()
    user_agent = event.get("headers", {}).get("user-agent", "Unknown")

    
    try:
        # Lookup geo info
        geo_response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        geo_data = geo_response.json()

        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")
        visit_date = datetime.utcnow().strftime('%Y-%m-%d')
        dedupe_key = f"{ip}#{visit_date}"
        expire_time = int(time.time()) + 86400  # 24 hours from now


        # DynamoDB write
        table_name = os.environ["DYNAMO_TABLE_NAME"]
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)

        item = {
            "ip_date_key": {"S": dedupe_key},
            "ip_address": {"S": ip},
            "visit_date": {"S": visit_date},
            "visit_time": {"S": datetime.utcnow().isoformat()},
            "country": {"S": country},
            "region": {"S": region},
            "city": {"S": city},
            "org": {"S": org},
            "user_agent": {"S": user_agent},
            "expire_time": {"N": str(expire_time)}
        }

        print("Writing to table:", table_name)
        print("Item being written:", json.dumps(item, indent=2))
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
        print("Error during Lambda execution:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
    try:
        dynamodb.put_item(
            TableName='GeoVisitors',
            Item=item,
            ConditionExpression='attribute_not_exists(ip_date_key)'
        )
        print(f"Visitor {ip} on {visit_date} recorded.")
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(f"Visitor {ip} already recorded today — skipping.")

    # 3. Return a success response
    return {
        "statusCode": 200,
        "body": "Visit recorded"
    }
