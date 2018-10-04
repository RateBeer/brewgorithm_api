#!/bin/bash
set -ev

case "$TRAVIS_BRANCH" in
"dev")
    AWS_ECS_REGION=${DEV_AWS_ECS_REGION}
    AWS_ECS_CLUSTER=${DEV_AWS_ECS_CLUSTER}
    ;;
"master")
    AWS_ECS_REGION=${MASTER_AWS_ECS_REGION}
    AWS_ECS_CLUSTER=${MASTER_AWS_ECS_CLUSTER}
    ;;
*)
    exit 1; # Unsupported deployment branch.
    ;;
esac

IMAGE_NAME=brewgorithm-api-${TRAVIS_BUILD_NUMBER}-prod
VERSION_TAG="${TRAVIS_BRANCH}-${TRAVIS_BUILD_NUMBER}"
LATEST_TAG="${TRAVIS_BRANCH}-latest"
IMAGE_NAME_WITH_VERSION_TAG="${DOCKER_IMAGE_NAME}:${VERSION_TAG}"
IMAGE_NAME_WITH_LATEST_TAG="${DOCKER_IMAGE_NAME}:${LATEST_TAG}"

# Build the Production-ready image
docker build -t ${IMAGE_NAME} .

# Instal AWS CLI w/o sudo
pip install --user awscli
export PATH=$PATH:$HOME/.local/bin

# Login to AWS ECR
eval $(aws ecr get-login --region ${AWS_ECR_REGION} --no-include-email)

# Create Docker Tags
docker tag ${IMAGE_NAME} ${AWS_ECR_ACCOUNT_ID}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com/${IMAGE_NAME_WITH_VERSION_TAG}
docker tag ${IMAGE_NAME} ${AWS_ECR_ACCOUNT_ID}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com/${IMAGE_NAME_WITH_LATEST_TAG}

# Push up the image
docker push ${AWS_ECR_ACCOUNT_ID}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com/${IMAGE_NAME_WITH_VERSION_TAG}
docker push ${AWS_ECR_ACCOUNT_ID}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com/${IMAGE_NAME_WITH_LATEST_TAG}

# Deploy the image with ECS-deploy; roll back upon failure.
docker run -e AWS_DEFAULT_REGION=${AWS_ECS_REGION} -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} silintl/ecs-deploy --use-latest-task-def -c ${AWS_ECS_CLUSTER} -n ${AWS_ECS_SERVICE_NAME} -to ${VERSION_TAG} -i ignore -t 3600 -r ${AWS_ECS_REGION} --enable-rollback


# Register the deploy
case "$TRAVIS_BRANCH" in
"master")
    curl -X POST -H 'Content-type: application/json' "https://6nipussq0m.execute-api.us-east-1.amazonaws.com/dev/deployment_efficiency/deployments?projectname=RateBeer&version=${TRAVIS_COMMIT}&reponame=brewgorithm_api&token=3p1uSSValUYMlvM" || exit 0
    ;;
*)
esac
