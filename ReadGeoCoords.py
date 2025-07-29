import json
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])

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
        resp = table.scan(
            FilterExpression=Attr("latitude").exists() & Attr("longitude").exists()
        )
        items = resp.get("Items", [])
        # clean all Decimal values first
        cleaned_items = clean_decimals(items)

        # map into the shape the frontend expects
        mapped = [{
            "lat": itm.get("latitude"),
            "lng": itm.get("longitude"),
            "city": itm.get("city", "Unknown"),
            "org": itm.get("org", "Unknown"),
            "timestamp": itm.get("visit_time", "")
        } for itm in cleaned_items]

        # <-- RETURN MAPPED, not 'cleaned' which doesn't exist
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(mapped)
        }

    except Exception as e:
        # log full traceback for debugging
        import traceback; traceback.print_exc()
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e),
                "type": type(e).__name__
            })
        }
