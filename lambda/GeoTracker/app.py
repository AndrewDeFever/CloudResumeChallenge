import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

import boto3


dynamodb = boto3.client("dynamodb")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": os.environ["CORS_ORIGIN"],
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def lookup_ip(ip):
    request = urllib.request.Request(
        f"https://ipinfo.io/{ip}/json",
        headers={"User-Agent": "CloudResumeChallenge/1.0"},
    )
    with urllib.request.urlopen(request, timeout=5) as result:
        return json.loads(result.read().decode("utf-8"))


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "OPTIONS":
        return response(200, {"message": "CORS preflight success"})

    ip = (
        event.get("headers", {}).get("x-forwarded-for")
        or event.get("requestContext", {}).get("http", {}).get("sourceIp")
    )
    if not ip:
        return response(400, {"message": "IP address could not be resolved; write skipped."})

    ip = ip.split(",")[0].strip()
    user_agent = event.get("headers", {}).get("user-agent", "Unknown")

    try:
        geo_data = lookup_ip(ip)
        coords = geo_data.get("loc", "0,0").split(",")
        latitude = float(coords[0])
        longitude = float(coords[1])

        now = datetime.now(timezone.utc)
        visit_date = now.strftime("%Y-%m-%d")
        dedupe_key = f"{ip}#{visit_date}"

        item = {
            "ip_date_key": {"S": dedupe_key},
            "ip_address": {"S": ip},
            "visit_date": {"S": visit_date},
            "visit_time": {"S": now.isoformat()},
            "country": {"S": geo_data.get("country", "Unknown")},
            "region": {"S": geo_data.get("region", "Unknown")},
            "city": {"S": geo_data.get("city", "Unknown")},
            "org": {"S": geo_data.get("org", "Unknown")},
            "user_agent": {"S": user_agent},
            "expire_time": {"N": str(int(time.time()) + 86400)},
            "latitude": {"N": str(latitude)},
            "longitude": {"N": str(longitude)},
        }

        dynamodb.put_item(
            TableName=os.environ["DYNAMO_TABLE_NAME"],
            Item=item,
            ConditionExpression="attribute_not_exists(ip_date_key)",
        )
        return response(200, {"message": "Geo data stored successfully"})

    except dynamodb.exceptions.ConditionalCheckFailedException:
        return response(200, {"message": "Visit already recorded today"})
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        print(f"Geolocation error: {exc}")
        return response(502, {"message": "Unable to resolve visitor geolocation"})
    except Exception as exc:
        print(f"Unhandled error: {exc}")
        return response(500, {"message": "Internal Server Error"})
