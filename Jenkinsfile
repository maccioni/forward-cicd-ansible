pipeline {
    agent any

    stages {
        stage('Stage 1') {
            echo 'Starting stage 1...'
            steps {
                sh "echo 'stage 1'"
            }
        }
        stage('Stage 2') {
            echo 'Starting stage 1...'
            steps {
                sh "echo 'stage 2'"
            }
        }
        stage('Stage 3') {
            echo 'Starting stage 3...'
            steps {
                sh "echo 'stage 3'"
            }
        }
        stage('Stage 4') {
            steps {
                echo 'Starting stage 4...'
                script {
                    try {
                        sh "echo 'stage 4: testing...'"
                    } catch (error) {
                        sh "echo 'stage 4: Error. Rolling back...'"
                        error("Changes failed testing.  Rolled back.")
                    }
                }
            }
        }
        stage('Copy run-start') {
            steps {
                sh "/opt/puppetlabs/bin/puppet-task run yang_ietf::saveconfig target='cat9k-puppet' --nodes 'cisco-pe-demo.localhost'"
            }
        }
    }
}
