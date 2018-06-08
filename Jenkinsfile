library 'Utilities'

// Only save the last 5 builds for each branch.
// Builds & logs from a branch will be automatically removed when the branch is removed
// (Although a re-scan may be necessary)
properties([
    buildDiscarder(logRotator(numToKeepStr: '5')),

    // Building at the same time can cause race conditions if we're deploying; build
    // one at a time.
    disableConcurrentBuilds()
])

node("ubuntu-docker") {
  linuxCleanup()
  checkout scm

  try {
    notifyBuild('STARTED')
    prepareAndRunCI()
  } catch (e) {
    // If there was an exception thrown, the build failed
    currentBuild.result = "FAILED"
    throw e
  } finally {
    linuxCleanup()

    // Success or failure, always send notifications
    notifyBuild(currentBuild.result)
  }
}

def prepareAndRunCI() {
  // Define the variables to be used
  String IMAGE_NAME          // The Docker image name we are building and deploying.
  String IMAGE_NAME_TEMP     // Temporary image name so multiple builds do not clash.
  String VERSION_TAG         // The version tag for this Docker image            (Dependent on branch).
  String LATEST_TAG          // The 'latest' tag for this Docker image           (Dependent on branch).
  String CI_TAG              // What we will tag the initial build as.
  String DOCKER_HOST         // The Docker Swarm host we are deploying to        (Dependent on branch).
  String ENVIRONMENT_NAME    // The environment we are marked as                 (Dependent on branch).
  String ECR_REPOSITORY      // The Elastic Container Registry Repository
  String ECR_REGION          // The Elastic Container Registry Region
  String ECS_REGION          // The ECS Region the cluster is in.
  String ECS_CLUSTER         // The name of the ECS Cluster
  String ECS_SERVICE_NAME    // The ECS Service Name

  ECS_SERVICE_NAME_READ  = "brewgorithm-api-read"
  ECS_SERVICE_NAME_WRITE = "brewgorithm-api-write"
  IMAGE_NAME       = "brewgorithm-api"
  IMAGE_NAME_TEMP  = "${IMAGE_NAME}-${env.BRANCH_NAME.toLowerCase()}-${env.BUILD_NUMBER}"
  CI_TAG           = "ci-latest"
  ECR_REPOSITORY   = "${env.ECR_REPOSITORY_URI_BASE}"
  ECR_REGION       = "${env.ECR_REPOSITORY_REGION}"

  switch (env.BRANCH_NAME) {
    // Set our variables as appropriate for the branch we're on.
    case "migration":
      VERSION_TAG      = "d1.${env.BUILD_NUMBER}"
      LATEST_TAG       = "dlatest"
      ENVIRONMENT_NAME = "qa"
      REACT_APP_ENV    = "qa"
      ECS_REGION       = "${env.QA_AWS_REGION}"
      ECS_CLUSTER      = "${env.QA_ECS_CLUSTER}"
      break;
    case "master":
      VERSION_TAG      = "m1.${env.BUILD_NUMBER}"
      LATEST_TAG       = "latest"
      ENVIRONMENT_NAME = "prod"
      REACT_APP_ENV    = "production"
      ECS_REGION       = "${env.PROD_AWS_REGION}"
      ECS_CLUSTER      = "${env.QA_ECS_CLUSTER}"
      break;
    default:
      break;
  }

    // Login to ECR so that we may access the base image and later push the built
    // image up.
    stage("Login to AWS Registry") {
      loginToAWSRegistry(ECR_REGION)
    }

    // Tests are run as a part of the Docker image
    stage("Build") {
      // The base image is stored in ECR us-west-2; login prior so we may pull it.
      loginToAWSRegistry(ECR_REGION)
      sh "docker build -t ${IMAGE_NAME_TEMP} ."
    }

    // Continuous deployment will only be setup for `dev` and `master` branches.
    if ( (env.BRANCH_NAME == "dev") || (env.BRANCH_NAME == "master") ) {

      stage("Push To Registry") {
        sh "docker tag ${IMAGE_NAME_TEMP} ${IMAGE_NAME}:${CI_TAG}"
        pushToDockerRegistry(IMAGE_NAME, ECR_REPOSITORY, CI_TAG, VERSION_TAG, LATEST_TAG)
      }

      stage("Deploy read API to ${ENVIRONMENT_NAME}") {
        // Deploy to ECS; rollback on failure.
        try {
          deployECSImageTag(ECS_REGION, ECS_CLUSTER, ECS_SERVICE_NAME_READ, VERSION_TAG, true)
        } catch(e) {
          error 'Deployment failed; previous version has been restored.'
        }
      }

      stage("Deploy write API to ${ENVIRONMENT_NAME}") {
        // Deploy to ECS; rollback on failure.
        try {
          deployECSImageTag(ECS_REGION, ECS_CLUSTER, ECS_SERVICE_NAME_WRITE, VERSION_TAG, true)
        } catch(e) {
          error 'Deployment failed; previous version has been restored.'
        }
      }
    }
}
