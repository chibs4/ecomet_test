#!/bin/bash

# Variables
PARSER_DIR="./parser"
ZIP_FILE="function.zip"
FUNCTION_NAME="github-parser"
TRIGGER_NAME="parser-trigger"
ENV_FILE="$PARSER_DIR/.env"
#Нужно задать
SERVICE_ACCOUNT_ID= 

# Zip the parser directory
echo "Zipping the parser directory..."
zip -r $ZIP_FILE $PARSER_DIR -x "$PARSER_DIR/$ZIP_FILE"

# Check if the zip operation was successful
if [ $? -ne 0 ]; then
  echo "Failed to zip the directory."
  exit 1
fi

echo "Zip created successfully."

# Create or update the function
echo "Creating/updating the function..."
yc serverless function create --name $FUNCTION_NAME

# Deploy the function version
echo "Deploying the function version..."
yc serverless function version create \
  --function-name $FUNCTION_NAME \
  --runtime python312 \
  --entrypoint main.main \
  --memory 128M \
  --execution-timeout 60s \
  --source-path $ZIP_FILE

# Add environment variables
# echo "Adding environment variables..."
# while IFS='=' read -r key value; do
#   if [ ! -z "$key" ]; then
#     yc serverless function version update \
#       --function-name $FUNCTION_NAME \
#       --environment "$key=$value"
#   fi
# done < $ENV_FILE

# Create a cron trigger
echo "Creating the cron trigger..."
yc serverless trigger create timer \
  --name $TRIGGER_NAME \
  --cron-expression "1 0 ? * * *" \
  --invoke-function-name $FUNCTION_NAME \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID
echo "Function and cron trigger created successfully."

