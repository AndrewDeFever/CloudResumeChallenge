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

| Feature                | Technology                                   |
|------------------------|-----------------------------------------------|
| Static Hosting         | S3, CloudFront, Route 53                      |
| HTTPS                  | ACM + CloudFront                              |
| Visitor Logging        | Lambda (`GeoTracker.py`) + DynamoDB          |
| Visitor Stats API      | Lambda (`ReadGeoStats`) + API Gateway        |
| Frontend Integration   | JavaScript + Flag/ISP Icons (Font Awesome)   |
| Infrastructure as Code | CloudFormation (YAML)                         |
| CI/CD                  | GitHub Actions with OIDC                      |
| IAM Security           | Scoped Lambda execution roles                |
| Python Version         | 3.13                                          |
| Testing                | Pytest (`tests/test_geo.py`)                 |

---

## 🧪 Testing

- Unit tests are written using `pytest`
- Executed automatically via GitHub Actions CI/CD pipeline

---

## 🔒 Security Notes

- **AWS Authentication**: GitHub Actions authenticate to AWS using OIDC (OpenID Connect), eliminating long-term credentials.
- **Least Privilege IAM**: IAM roles and policies are scoped to only what's required for each function.
- **Scoped Lambda Permissions**: Lambdas are protected by resource-based permissions and are not publicly invokable.
- **No Hardcoded Secrets**: Configuration (e.g., table names) is stored in environment variables.
- **No Secrets Required**: No AWS access keys, tokens, or API keys are stored or needed.
- **CORS & API Hardening**: CORS is configured; future work includes adding IP allowlisting or token protection.

---

## 🌐 Live Demo

🔗 [https://www.subrealstudios.com/CloudResumeChallenge.html](https://www.subrealstudios.com/CloudResumeChallenge.html)

---

## 🔭 Future Enhancements

- [x] Add `ReadGeoStats` Lambda to fetch and expose visitor data via API Gateway
- [x] Implement frontend integration with dynamic flags and ISP icons
- [x] Secure CI/CD using GitHub Actions with OpenID Connect (OIDC) authentication
- [x] Deduplicate or group visits by IP (e.g., daily unique count)
- [x] Add request throttling or basic abuse protection (e.g., API Gateway usage plans)
- [ ] Expand CloudFormation template to cover full infrastructure deployment (S3, CloudFront, Route 53, IAM, etc.)
- [ ] Add monitoring and alarms for Lambda duration, error rate, and DynamoDB capacity

## 📜 License

GNU General Public License
