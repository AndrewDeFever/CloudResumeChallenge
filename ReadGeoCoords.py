import json
import boto3
import os
import decimal        
import traceback

traceback.print_exc()

from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

# Recursively convert Decimal to float or int
def clean_decimals(obj):
    if isinstance(obj, list):
        return [clean_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: clean_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://www.subrealstudios.com",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        response = table.scan(
            FilterExpression=Attr("latitude").exists() & Attr("longitude").exists()
        )

        items = response.get("Items", [])
        cleaned_items = clean_decimals(items)

        mapped = []

        for item in cleaned_items:
            mapped.append({
                "lat": item.get("latitude"),
                "lng": item.get("longitude"),
                "city": item.get("city", "Unknown"),
                "org": item.get("org", "Unknown"),
                "timestamp": item.get("visit_time", "")
            })


        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(cleaned)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e),
                "type": type(e).__name__
            })
        }
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
