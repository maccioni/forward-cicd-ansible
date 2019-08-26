pipeline {
    agent any

    stages {
        stage('Download code from GitHub') {
            steps {
                sh "echo 'stage 1'"
            }
        }
        stage('Test Ansible Playbook') {
            steps {
                sh "ansible-playbook ansible-test.yml -vvvv"
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
        stage('Stage 5') {
            steps {
                sh "echo 'stage 5...'"
            }
        }
    }
}
