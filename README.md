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

🔒 Security Notes
- AWS Authentication: GitHub Actions authenticate to AWS using OIDC (OpenID Connect), eliminating the need to store long-term AWS credentials.
- Least Privilege IAM: All IAM roles and policies are designed using the Principle of Least Privilege, granting only the specific permissions required by each component.
- Scoped Lambda Permissions: Lambda functions use resource-based policies to restrict access to DynamoDB tables and are not publicly invokable.
- No hardcoded secrets: Sensitive configurations like table names are passed through environment variables, not embedded in code.
- No secrets required: This project does not use AWS access keys, tokens, or API keys. OIDC and IAM policies eliminate the need for credential storage.
- CORS & API Hardening: Cross-Origin Resource Sharing (CORS) is explicitly configured. Further enhancements (e.g., IP allowlisting, API keys) are listed in the Future Enhancements section.

## 🌐 Live Demo

View it here:  
**[https://www.subrealstudios.com/CloudResumeChallenge.html](https://www.subrealstudios.com/CloudResumeChallenge.html)**

## 🔭 Future Enhancements

- [x] Add `ReadGeoStats` Lambda to fetch and expose visitor data via API Gateway
- [x] Implement frontend integration with dynamic flags and ISP icons
- [x] Secure CI/CD using GitHub Actions with OpenID Connect (OIDC) authentication
- [ ] Deduplicate or group visits by IP (e.g., daily unique count)
- [ ] Add request throttling or basic abuse protection (e.g., API Gateway usage plans)
- [ ] Optionally secure API routes using IAM auth or API Gateway token auth
- [ ] Integrate AWS Secrets Manager (if future API keys or credentials are introduced)
- [ ] Expand CloudFormation template to cover full infrastructure deployment (S3, CloudFront, Route 53, IAM, etc.)
- [ ] Add monitoring and alarms for Lambda duration, error rate, and DynamoDB capacity

## 📜 License

MIT License
