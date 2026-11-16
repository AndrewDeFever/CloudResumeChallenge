#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${STACK_NAME:-CloudResume-App}"
REGION="${AWS_REGION:-us-east-1}"
TEMPLATE="${TEMPLATE:-AWS_CF_Templates/CloudResumeApp.yml}"

echo "Validating ${TEMPLATE}..."
aws cloudformation validate-template \
  --template-body "file://${TEMPLATE}" \
  --region "${REGION}" > /dev/null

echo "Deploying ${STACK_NAME}..."
aws cloudformation deploy \
  --stack-name "${STACK_NAME}" \
  --template-file "${TEMPLATE}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "${REGION}" \
  --no-fail-on-empty-changeset

echo "Stack outputs:"
aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --query 'Stacks[0].Outputs[].{Key:OutputKey,Value:OutputValue}' \
  --output table
