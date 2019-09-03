pipeline {
    agent any

    stages {
        stage('Download code from GitHub') {
            steps {
                echo "Downloaded code from https://github.com/maccioni/forward-cicd-ansible"
                sh 'env'
                slackSend (message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})", username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
            }
        }
        stage('Pre-change validation') {
            steps {
                sh "echo 'Checking if the policy is already in place. If it is, exit successfully.'"
                sh "ansible-playbook pre-change-validation.yml"
                sh "python pre-change-validation.py"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Simulate change in Sandbox') {
            steps {
                sh "echo 'Placeholder for policy simulation on Forward Sandbox'"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Apply network change') {
            steps {
                sh "ansible-playbook ansible-test.yml -vvvv"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Post-change validation') {
            steps {
                script {
                    try {
                        sh "echo 'Placeholder for Post-change validation'"
                        echo "currentBuild.currentResult: ${currentBuild.currentResult}"
                    } catch (error) {
                        error("Changes failed testing.  Rolled back.")
                        echo "currentBuild.currentResult: ${currentBuild.currentResult}"
                    }
                }
            }
        }
    }
    post {
        always {
            echo "(Post always) currentBuild.currentResult: ${currentBuild.currentResult}"
            echo "(Post always) currentBuild.Result: ${currentBuild.result}"
        }
        success {
            echo "(Post success) Pipeline executed successfully!"
            slackSend (message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})", color: '#00FF00', username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
        }
        unstable {
            echo "(Post unstable) Pipeline is unstable :/"
        }
        failure {
            echo "(Post failure) Pipeline Failed!!!"
            slackSend (message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})", color: '#FF0000', username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
        }
        changed {
            echo "(Post failure) Something changed..."
        }
    }
}
