#!/usr/bin/env bash

# Deploy Lambda function to Ireland region
usage() {
  echo "Usage: $0 LAMBDA_FUNCTION_NAME"
  echo "Example: $0 TruebrandPostShare"
  exit 1
}

if [ $# -lt 1 ] ; then
  usage
fi

FUNCTION_NAME="$1"
REGION="eu-west-1"  # Ireland
REQUIREMENTS_FILE="requirements.txt"

echo "🚀 Deploying $FUNCTION_NAME to $REGION..."

set -e

# Clean up previous builds
echo "🧹 Cleaning up..."
rm -rf dist || true
rm -rf env || true

# Create virtual environment and install dependencies
echo "📦 Installing dependencies..."
python3 -m venv env
source env/bin/activate
pip install --upgrade pip --index-url https://pypi.org/simple/
pip install -r $REQUIREMENTS_FILE --target dist/ --index-url https://pypi.org/simple/

# Copy source code
echo "📁 Copying source code..."
cp -rf src dist/

# Create deployment package
echo "📦 Creating deployment package..."
rm -f /tmp/truebrand-deployment.zip || true
cd dist && zip -r9 /tmp/truebrand-deployment.zip .

# Update Lambda function with zip file
echo "⚡ Updating Lambda function..."
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb:///tmp/truebrand-deployment.zip \
  --publish \
  --region $REGION

echo "✅ Deployment complete!"
echo "🔗 Function: $FUNCTION_NAME"
echo "🌍 Region: $REGION"


