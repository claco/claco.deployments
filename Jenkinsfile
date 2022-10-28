pipeline {
  agent any

  stages {
    stage("CowSay") {
      steps {
        sh 'echo "moo"'
      }
    }
    stage("DockerSay") {
      agent {
        docker {
          image "docker/whalesay:latest"
        }
      }

      steps {
        sh "cowsay moo"
      }
    }
  }

  post{
    always{
      cleanWs(disableDeferredWipeout: true, notFailBuild: true)
    }
  }
}
