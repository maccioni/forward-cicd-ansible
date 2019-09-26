pipeline {
    agent any

    stages {
        stage('Initial Stage') {
          steps {
              echo "Check enviroment "
              sh "env"
            }
        }
        stage("Gather Deployment Parameters") {
            steps {
                timeout(time: 60, unit: 'SECONDS') {
                    script {
                        def user_inputs = input message: 'User input required', ok: 'Enter',
                            parameters: [
                               string(defaultValue: '', description: 'Service Name', name: 'name'),
                               string(defaultValue: '', description: 'Service IP', name: 'ip'),
                               string(defaultValue: '', description: 'Service port', name: 'port')
                            ]
                    }
                    env.SERVICE_NAME = user_inputs.name
                    env.SERVICE_IP = user_inputs.ip
                    env.SERVICE_PORT = user_inputs.port
                    echo "${env.SERVICE_NAME}"
                    echo "${env.SERVICE_IP}"
                    echo "${env.SERVICE_PORT}"
                }
            }
        }
        stage("Use Deployment Parameters") {
         steps {
                script {
                    echo "All parameters have been set as Environment Variables"
                    echo "Service name: ${env.SERVICE_NAME}"
                    echo "Service IP: ${env.SERVICE_IP}"
                    echo "Service IP: ${env.SERVICE_PORT}"
                    }
                }
        }
        stage('Final Stage') {
            steps {
              echo "Check enviroment "
              sh "env"
            }
        }
    }
}
