import json
import boto3
import os
from datetime import datetime
import requests

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        headers = event.get("headers", {})
        ip = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for")

        if not ip:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "IP address not found in headers"})
            }

        # Use ipinfo.io to get geo data
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        geo_data = response.json()

        country = geo_data.get("country", "Unknown")
        region = geo_data.get("region", "Unknown")
        city = geo_data.get("city", "Unknown")
        org = geo_data.get("org", "Unknown")

        # Store in DynamoDB
        table.put_item(Item={
            'ip_address': ip,
            'visit_time': datetime.utcnow().isoformat(),
            'country': country,
            'region': region,
            'city': city,
            'org': org
        })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Geo data stored",
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
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
