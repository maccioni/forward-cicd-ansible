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
                echo "Getting Path info using Ansible URI module (TBD build a forward_path module)"
                sh "ansible-playbook pre-change-validation.yml"
                echo "Checking if routing and policies are already in place for the given path"
                sh "python pre-change-validation.py"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Simulate change in Sandbox') {
            steps {
                echo "Creating a new IntentCheck for the given Path"
                echo "Changing security policy in the Forward Sandbox (TBD work with Nikhil on Sandbox internal REST APIs)"
                echo "Saving changes in Sandbox"
                echo "Analyze changes"
                echo "Verify Check status "
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Apply network change') {
            steps {
                echo "Push changes to production using Ansible playbook (TBD replace ios playbbok with panos)"
                sh "ansible-playbook ansible-test.yml -vvvv"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Post-change validation') {
            steps {
                echo "Collect from modified devices only (TBD work with Brandon/Santhosh? on Partial Collection internal REST APIs)"
                echo "Get all Checks using Ansible URI module and (TBD enhance forward_check module to get all the Checks??)"
                sh "ansible-playbook post-change-validation.yml"
                echo "Verify all Checks"
                sh "python post-change-validation.py"
                echo("Some Checks are failing.  Rolling back configuration. (TBD implement rollback)")
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
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
            slackSend (message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})", color: '#00FF00', username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
        }
        unstable {
            echo "(Post unstable) Pipeline is unstable :/"
        }
        failure {
            echo "(Post failure) Pipeline Failed!!!"
            slackSend (message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})", color: '#FF0000', username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
        }
        changed {
            echo "(Post failure) Something changed..."
        }
    }
}
