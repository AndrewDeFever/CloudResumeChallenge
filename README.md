# ☁️ Cloud Resume Challenge — GeoTracker Edition

A serverless web resume hosted on AWS using S3, CloudFront, and Route 53, with a dynamic visitor tracking feature powered by Lambda, API Gateway, and DynamoDB.

## 📁 Directory Structure

```
.
├── .github/workflows/
│   ├── deploy.yml
│   └── CloudResumeChallengeDeploy.yml
├── AWS_CF_Templates/
│   └── GeoTrackerLambdaStack.yml
├── tests/
│   ├── __init__.py
│   └── test_geo.py
├── CloudResumeChallenge.html
├── vendor/                  # Vendored mapping dependencies
├── docs/PRODUCTION-ARCHITECTURE.md
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
| Visitor Stats API      | Lambda (`ReadGeoCoords`) + API Gateway        |
| Frontend Integration   | JavaScript + Flag/ISP Icons (Font Awesome)   |
| Infrastructure as Code | CloudFormation (YAML)                         |
| CI/CD                  | GitHub Actions with OIDC                      |
| IAM Security           | Scoped Lambda execution roles                |
| Python Version         | Verify deployed runtime in AWS (IaC source uses 3.12)                                          |
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

🔗 [https://resume.subrealstudios.com/](https://resume.subrealstudios.com/)

Production serves **CloudFront E11F2W61OQF97D** → **S3 bucket `resume.subrealstudios.com`** → **`index.html`**. GitHub's `CloudResumeChallenge.html` is published as `index.html`. See [Production architecture and deployment](docs/PRODUCTION-ARCHITECTURE.md) for the verified origin, deploy workflow, asset gaps, IAM prerequisites, and rollback.

---

## 🔭 Future Enhancements

- [x] Add `ReadGeoCoords` Lambda to fetch and expose visitor data via API Gateway
- [x] Implement frontend integration with dynamic flags and ISP icons
- [x] Secure CI/CD using GitHub Actions with OpenID Connect (OIDC) authentication
- [x] Deduplicate or group visits by IP (e.g., daily unique count)
- [x] Add request throttling or basic abuse protection (e.g., API Gateway usage plans)
- [ ] Expand CloudFormation template to cover full infrastructure deployment (S3, CloudFront, Route 53, IAM, etc.)
- [ ] Add monitoring and alarms for Lambda duration, error rate, and DynamoDB capacity

## 📜 License

GNU General Public License
