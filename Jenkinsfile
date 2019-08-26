pipeline {
    agent any

    stages {
        stage('Stage 1') {
            steps {
                sh "echo 'stage 1'"
            }
        }
        stage('Stage 2') {
            steps {
                sh "echo 'stage 2'"
            }
        }
        stage('Stage 3') {
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
        stage('Stsage 5') {
            steps {
                sh "echo 'stage 5...'"
            }
        }
    }
}
