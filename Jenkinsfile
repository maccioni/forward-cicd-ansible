pipeline {
    agent any

    stages {
        stage('Download code from GitHub') {
            steps {
                echo "Downloaded code from https://github.com/maccioni/forward-cicd-ansible"
                sh 'env'
                sh "cp intent_check_new_service.yml fwd-ansible"
                slackSend (message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})",  username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'fwd-net', channel: 'demo-notifications')
            }
        }
        stage('Check if change is needed') {
            steps {
                echo "Getting Path info using Ansible URI module"
                sh "ansible-playbook get_path.yml"
                echo "Checking if routing and policies are already in place for the given path"
                sh "python is_change_needed.py"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Verify change in Sandbox') {
//            when {
//                Proceed only if Only say hello if a "greeting" is requested
//                expression { ${env.JENKINS_IS_CHANGE_NEEDED} == 'TRUE' }
//            }
            steps {
                echo "Change security policy in the Forward Sandbox"
                sh "ansible-playbook save_changes_in_sandbox.yml -vvvvv"
                echo "Creating a new IntentCheck for the new service"
                sh "ansible-playbook fwd-ansible/intent_check_new_service.yml --extra-vars=expected_check_status=FAIL -vvvvv"
                echo "Get all Checks using Ansible URI module"
                sh "ansible-playbook get_checks.yml"
                script {
                    try {
                        echo "Verify all Checks"
                        sh "python verify_checks.py"
                    } catch (error) {
                        echo("Some Checks are failing.  Failing the pipeline and exiting.")
                        sh "ansible-playbook rollback_changes.yml -vvvv"
                    }
                }
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Apply network change to production') {
            steps {
                echo "Push changes to production using Ansible playbook)"
                sh "ansible-playbook deploy_changes.yml -vvvv"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Verify new connectivity and check for regressions') {
            steps {
                echo "Collect from modified devices only and make sure collection and processing are over"
                sh "ansible-playbook take_partial_collection.yml -vvvv"
                echo "Get all Checks using Ansible URI module"
                sh "ansible-playbook get_checks.yml"
                script {
                    try {
                        echo "Verify all Checks"
                        sh "python verify_checks.py"
                    } catch (error) {
                        echo("Some Checks are failing.  Rolling back configuration.")
                        sh "ansible-playbook rollback_changes.yml -vvvv"
                    }
                }
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
