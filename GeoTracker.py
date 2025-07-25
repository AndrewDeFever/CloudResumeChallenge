import json
import boto3
import os
from datetime import datetime
import requests

# Set up DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        # Get the IP address from headers
        headers = event.get("headers", {})
        ip = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for")

        if not ip:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "https://subrealstudios.com"
                },
                "body": json.dumps({"error": "IP address not found in headers"})
            }

        # Call ipinfo.io to get geolocation data
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        geo_data = response.json()

        # Extract useful info
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
            "org": org
        })

        # Successful response
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "https://subrealstudios.com"
            },
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

        print(f"GeoTracker ERROR: {str(e)}")
        
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "https://subrealstudios.com"
            },
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
