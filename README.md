# 🌐 GeoTracker Lambda (Cloud Resume Challenge - Full Stack Serverless App)

This is a full-stack, production-ready serverless web application built as part of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/). It includes:

- A static frontend hosted on Amazon S3 behind CloudFront with SSL (HTTPS)
- A backend Lambda function triggered by the frontend
- Visitor IP and geolocation data are stored in DynamoDB
- Secure CI/CD pipeline using GitHub Actions and scoped IAM access

---

## 🚀 Features

- 🌍 **Frontend** hosted on Amazon S3
- 🔒 **Secured with CloudFront + SSL (HTTPS)**
- 🛰️ **AWS Lambda** receives client IP + geolocation
- 🧠 **Amazon DynamoDB** stores visitor metadata
- 🔐 **IAM** scoped for least-privilege GitHub Actions deployment
- ⚙️ **CI/CD** automated with GitHub Actions and `deploy.yml`

---

## 🛠️ Technologies Used

| Service         | Purpose                               |
|-----------------|----------------------------------------|
| AWS Lambda      | Serverless backend logic               |
| Amazon DynamoDB | Persistent NoSQL storage               |
| Amazon S3       | Frontend static website hosting        |
| AWS CloudFront  | CDN + HTTPS SSL termination            |
| GitHub Actions  | Continuous Integration & Deployment    |
| IAM             | Secure AWS access for GitHub pipeline  |
| Python 3.11     | Lambda runtime                         |

---

## 📁 Project Structure

```
.
├── GeoTracker.py         # Lambda function
├── requirements.txt      # Python dependency list
└── .github/
    └── workflows/
        └── deploy.yml    # GitHub Actions CI/CD workflow
```

---

## ⚙️ CI/CD Workflow

When code is pushed to the `main` branch:

1. GitHub Actions installs dependencies from `requirements.txt`
2. Packages the Lambda function into a zip
3. Authenticates to AWS using GitHub Secrets
4. Deploys the package to the existing Lambda function

Secrets are configured in GitHub:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

---

## 🧠 What I Learned

- Serverless deployment best practices with AWS Lambda + DynamoDB
- Frontend hosting with S3 + CloudFront + SSL
- CI/CD automation with GitHub Actions
- Secure IAM role configuration for automation

---

## 📎 Future Improvements

- Add visitor dashboard using Athena + QuickSight
- Integrate unit tests into CI/CD pipeline
- Add alerting with CloudWatch Logs
- Use environment branching (dev → prod)

---

## 👋 Author

**Andrew DeFever**  
AWS Certified Cloud Practitioner | CompTIA Security+  
GitHub: [@AndrewDeFever](https://github.com/AndrewDeFever)  
LinkedIn: [linkedin.com/in/andrewdefever](https://linkedin.com/in/andrewdefever)
