pipeline {
  agent any
  stages {
    stage('Deps') {
      steps {
        sh 'docker-compose -f docker-compose.deps.yml run --rm pip'
        sh 'docker-compose -f docker-compose.deps.yml run --rm assets'
      }
    }
    stage('') {
      steps {
        parallel(
          "Unit": {
            sh 'docker-compose -f docker-compose.tests.yml run --rm unit'
            
          },
          "Integration": {
            sh 'docker-compose -f docker-compose.tests.yml run --rm integration'
            
          }
        )
      }
    }
    stage('acceptance') {
      steps {
        sh 'docker-compose -f docker-compose.tests.yml run --rm acceptance'
      }
    }
  }
}