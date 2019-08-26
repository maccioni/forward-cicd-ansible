pipeline {
    agent any

    stages {
        stage('Download code from GitHub') {
            steps {
            }
        }
        stage('Pre-change validation') {
            steps {
                sh "echo 'Checking if the policy is already in place. If it is, exit successfully.'"
                echo "Pre-change validation result: ${currentBuild.result}"
                echo "Pre-change validation currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Pre-change validation') {
            steps {
                sh "echo 'Placeholder for Pre-change validation'"
            }
        }
        stage('Apply network change') {
            steps {
                sh "ansible-playbook ansible-test.yml -vvvv"
            }
        }
        stage('Post-change validation') {
            steps {
                script {
                    try {
                        sh "echo 'Placeholder for Post-change validation'"
                    } catch (error) {
                        error("Changes failed testing.  Rolled back.")
                    }
                }
            }
        }
    }
}
