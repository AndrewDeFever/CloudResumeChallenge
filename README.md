# 🌐 Cloud Resume Challenge – GeoTracker

This project extends the [Cloud Resume Challenge](https://cloudresumechallenge.dev/) by adding a serverless backend that geolocates each site visitor and stores data in DynamoDB using AWS Lambda, API Gateway, and CI/CD automation with GitHub Actions.

---

## 📐 Architecture

- **Frontend**: Static site hosted on S3 + CloudFront + SSL
- **Backend**: Python AWS Lambda triggered via API Gateway
- **Database**: DynamoDB for geolocation data
- **CI/CD**: GitHub Actions pipeline for test & deploy
- **Monitoring**: CloudWatch Logs & error alerts via SNS
- **Infrastructure as Code**: CloudFormation (optional)

---

### 📁 Project Structure

```text
CloudResumeChallenge/
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD pipeline (GitHub Actions)
│
├── tests/                        # Unit testing folder
│   ├── __init__.py               # Marks the folder as a Python package
│   └── test_geo.py               # Pytest unit test for GeoTracker Lambda
│
├── CloudResumeChallenge.html     # Frontend HTML file hosted on S3
├── GeoTracker.py                 # Lambda function for logging IP geodata
├── lambda_geoip.zip              # Zipped deployment package for Lambda (generated)
├── requirements.txt              # Python dependencies (e.g., boto3, requests)
├── LICENSE                       # License file for the project
└── README.md                     # This file
```

## 🧠 How It Works

1. Frontend calls a REST API endpoint
2. Lambda function:
   - Parses visitor IP from headers
   - Calls `ipinfo.io` to get location data
   - Stores the result in DynamoDB
3. Returns a JSON response

---

## 🧪 Testing
Unit tests use `pytest` with mocks for `boto3` and `requests`.

### Run Locally

bash
pip install -r requirements.txt
python -m pytest tests


🚀 CI/CD Pipeline
Automatically deploys Lambda function on push to main.

Workflow Steps
Set up Python 3.11

Install dependencies

Run unit tests

Package function as lambda.zip

Deploy via aws lambda update-function-code

Required GitHub Secrets
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY


🔐 Environment Variables
These must be configured in your Lambda function:

DYNAMO_TABLE_NAME=GeoVisitors
AWS_REGION=us-east-1


🔔 Monitoring
CloudWatch Logs enabled for Lambda

Alarm created for errors

SNS sends alerts (email, etc.)


🧱 Future Enhancements
 Add read/retrieve Lambda for visitor stats

 Deduplicate IPs or track unique daily visits

 Use Secrets Manager for IP info API token (if required)

 Finalize CloudFormation or CDK for full deployment

✅ Status
✅ Lambda deployed
✅ Tests mocked and passing
✅ CI/CD live via GitHub Actions
✅ Writes to DynamoDB working
🚧 CloudFormation in progress
