#!/bin/sh
set -o allexport
source .env
set +o allexport

echo "Bringing any previous instances down"
docker-compose down

echo "Starting localstack via Docker"
docker-compose up -d --build

echo "Sleeping for 15 seconds while localstack starts up"
sleep 15

SSM_ENDPOINT="http://docker.for.mac.localhost:4583"

# Note; the S3 API has an issue where it doesn't like docker.for.mac.localhost; so we use localhost and use --net=host
S3_ENDPOINT="http://localhost:4572"

echo "Creating S3 bucket"
docker run --net=host -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} cgswong/aws:latest aws --region ${S3_AWS_REGION} --endpoint-url=${S3_ENDPOINT} s3 mb s3://${S3_BUCKET}

echo "Creating SSM keys"
docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} cgswong/aws:latest aws --region ${SSM_AWS_REGION} --endpoint-url=${SSM_ENDPOINT} ssm put-parameter --name ${SSM_KEY_RATEBEER_DB_USER} --value "strongdm" --type String
docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} cgswong/aws:latest aws --region ${SSM_AWS_REGION} --endpoint-url=${SSM_ENDPOINT} ssm put-parameter --name ${SSM_KEY_RATEBEER_DB_PASS} --value "strongdm" --type SecureString
