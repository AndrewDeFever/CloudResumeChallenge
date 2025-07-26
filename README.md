# ☁️ Cloud Resume Challenge — GeoTracker Edition

A serverless web resume hosted on AWS using S3, CloudFront, and Route 53, with a dynamic visitor tracking feature powered by Lambda, API Gateway, and DynamoDB.

## 📁 Directory Structure

```
.
├── .github/workflows/
│   ├── deploy.yml
│   └── requirements.txt
├── AWS_CF_Templates/
│   └── GeoTrackerLambdaStack.yml
├── tests/
│   ├── __init__.py
│   └── test_geo.py
├── CloudResumeChallenge.html
├── GeoTracker.py
├── lambda_geoip.zip
├── LICENSE
├── README.md
└── requirements.txt
```

## 🚀 Tech Stack

| Feature               | Technology                                    |
|----------------------|-----------------------------------------------|
| Static Hosting        | S3, CloudFront, Route 53                      |
| HTTPS                 | ACM + CloudFront                              |
| Visitor Logging       | Lambda (GeoTracker) + DynamoDB               |
| Visitor Stats API     | Lambda (`ReadGeoStats`) + API Gateway        |
| Frontend Integration  | JavaScript + Flag/ISP Icons (FontAwesome)    |
| Infrastructure as Code| CloudFormation (YAML template)               |
| CI/CD                 | GitHub Actions with OIDC                      |
| IAM Security          | Scoped Lambda execution roles                |
| Python Version        | 3.13                                          |
| Testing               | Pytest (`tests/test_geo.py`)                 |

## 🧪 Testing

- Tests are run using `pytest`.
- GitHub Actions handles linting, testing, and deployment automatically.

## 🔐 Security Notes

- GitHub Actions use **OIDC** for AWS authentication (no stored secrets).
- IAM roles follow least privilege principles.
- Lambda access to DynamoDB is controlled via resource-based policies.

## 🌐 Live Demo

View it here:  
**[https://www.subrealstudios.com/CloudResumeChallenge.html](https://www.subrealstudios.com/CloudResumeChallenge.html)**

## ✅ Future Enhancements

- [x] Add `ReadGeoStats` Lambda to fetch visitor data
- [ ] Deduplicate IPs or limit by unique daily visits
- [ ] Secure API calls with token/IP allowlist
- [ ] Use AWS Secrets Manager for API key management
- [ ] Full deployment via CloudFormation or CDK

## 📜 License

MIT License
