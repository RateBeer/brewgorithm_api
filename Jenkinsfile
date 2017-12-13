import java.text.SimpleDateFormat

pipeline {
  agent {
    label "test"
  }
  options {
    buildDiscarder(logRotator(numToKeepStr: '2'))
    disableConcurrentBuilds()
  }
  stages {
    stage("build") {
      steps {
        script {
          def dateFormat = new SimpleDateFormat("yy.MM.dd")
          registry = 'brewgorithm'
          container = 'brewgorithm-api'
          stackName = 'brewgorithm'
          domain = 'api.brewgorithm.com'
          currentBuild.displayName = dateFormat.format(new Date()) + "-" + env.BUILD_NUMBER
          tag = currentBuild.displayName
        }
        sh "docker image build -t ${container} -f Dockerfile ."
      }
    }
    stage("release") {
      when {
        branch "master"
      }
      steps {
        dockerLogin()
        dockerTagAndPushImage(registry, container, 'latest')
        dockerTagAndPushImage(registry, container, tag)
        dockerLogout()
      }
    }
    stage("deploy") {
      when {
        branch "master"
      }
      agent {
        label "prod"
      }
      steps {
        dockerLogin()
        withEnv([
          "TAG=${tag}"
        ]) {
          sh "docker network create --driver overlay api || echo 'Network creation failed. It probably already exists.'"
          script {
            env.SERVICE_DOMAIN = domain
          }
          dockerStackDeployWithDomain(stackName, domain)
        }
        dockerLogout()
      }
    }
  }
  post {
    always {
      sh "docker system prune -f -a --volumes"
    }
    success {
      slackSend(
        color: "good",
        message: "${env.JOB_NAME} succeeded: ${env.RUN_DISPLAY_URL}"
      )
    }
    failure {
      slackSend(
        color: "danger",
        message: "${env.JOB_NAME} failed: ${env.RUN_DISPLAY_URL}"
      )
    }
  }
}