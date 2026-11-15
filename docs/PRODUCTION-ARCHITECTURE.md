# Production resume architecture and deployment

**State:** Confirmed via AWS CLI November 15, 2026. Refer to the Google Drive architecture document for the complete discovery log.

## Frontend request path

```text
https://resume.subrealstudios.com/
      |
      v
CloudFront E11F2W61OQF97D
  domain: d1p2hza69zkyiv.cloudfront.net
  default root: index.html
  origin access control: EYYS6WZWN3BVW
      |
      v
S3 bucket: resume.subrealstudios.com
  index.html
  styles.css
  architecture.svg
  background.png
  favicon.ico
  CloudResumeChallenge/ (resume and certificates)
  vendor/ (Leaflet, MarkerCluster, Leaflet.heat -- after repaired deploy)
```

The S3 origin is `resume.subrealstudios.com.s3.us-east-1.amazonaws.com`. No origin path is configured. The production HTML inspected on 2026-11-15 still referenced old CARTO tiles. Source `CloudResumeChallenge.html` has since been updated for Esri World Light Gray Canvas imagery and vendored map libraries.

**Important:** The *old* frontend workflow deployed to `s3://subrealstudios.com/CloudResumeChallenge.html`, a separate bucket and key that are not the root document for the resume hostname. The repaired workflow publishes `CloudResumeChallenge.html` as `s3://resume.subrealstudios.com/index.html` and `vendor/` to the **same** bucket, then invalidates the dedicated distribution.

## Deployment procedure

The GitHub Actions workflow `.github/workflows/CloudResumeChallengeDeploy.yml` uses GitHub OIDC to assume `arn:aws:iam::042889969210:role/GitHubOIDC-LambdaDeploy`.

1. Check the HTML has the Esri tile URL and all required vendored JS/CSS assets are present.
2. Authenticate to AWS via GitHub OIDC.
3. Validate the CloudFront distribution's origin and default root document; check existing production-only CSS/assets are present.
4. Download the existing `index.html` and store it as a 30-day GitHub Actions artifact for rollback.
5. Publish `CloudResumeChallenge.html` to the production bucket as `index.html`, sync the vendored map libraries, and invalidate `/`, `/index.html` and `/vendor/*`.

The workflow is automatic for scoped frontend changes on `main`, with a manual `workflow_dispatch` option. Lambda deployment is separately scoped to backend source/tests.

**Permission prerequisites (not yet confirmed for the OIDC role):** S3 write permissions in `resume.subrealstudios.com`; S3 read of the existing HTML and required assets; `cloudfront:GetDistribution` and `cloudfront:CreateInvalidation` for `E11F2W61OQF97D`. A workflow failure here is not evidence the frontend source is defective. Grant narrowly scoped IAM permissions after reviewing the actual failure and role policy.

## Repository and production gaps to close

- `styles.css` is not yet tracked at repository root (confirmed by GitHub file lookup), but does exist in the production bucket. The workflow **preserves** it; do not use a broad `aws s3 sync --delete` of the bucket. Import and review the stylesheet separately before making GitHub a complete static-site source of truth.
- Other existing objects include `architecture.svg`, `background.png`, `favicon.ico`, `geolocation.py`, and `CloudResumeChallenge/` resume/cert files. None are deleted by the deploy workflow. Inspect `geolocation.py` before deciding whether it should be exposed via the web.
- HTML references two API Gateway endpoints: `https://njx3tbb522.execute-api.us-east-1.amazonaws.com/track` and `https://lkqaj47w3b.execute-api.us-east-1.amazonaws.com/ReadGeoCoords`. GitHub deploys Lambda functions `GeoTracker` and `ReadGeoCoords`. Verify active API integration/permissions from AWS; don't infer them from filenames.
- Older CloudFormation notes mention `GeoVisitors` versus `GeoVisitorsByDay`; inspect live DynamoDB, IAM and Lambda settings before applying any infrastructure changes.

## Rollback and validation

A successful deploy exposes a workflow artifact named `previous-production-index-<run-id>` containing the old `index.html` for 30 days. To roll back, restore that artifact to `s3://resume.subrealstudios.com/index.html` and invalidate `/` and `/index.html`. Do not delete `vendor/` or other production assets as part of an HTML rollback.

Check the workflow run logs; verify `https://resume.subrealstudios.com/` responds successfully, loads `styles.css` and vendored map assets, draws Esri tiles (not CARTO), and displays visitor API results. The map tile service is third-party hosted; it is not copied into S3.

Production architecture baseline (Drive):
https://docs.google.com/document/d/1qLlHMNJqPNCuMjWOO63hq-DjO_taGuhekEbhzYx-Oj8/edit
