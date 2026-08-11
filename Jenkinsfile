pipeline {

    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                if not exist venv (
                    python -m venv venv
                )
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright Browser') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                python -m playwright install chromium
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat

                if not exist reports mkdir reports

                python -m pytest -v --junitxml=reports\\results.xml
                '''
            }
        }
    }

    post {

        always {

            junit allowEmptyResults: true,
                  testResults: 'reports/results.xml'

            archiveArtifacts artifacts: 'screenshots/**',
                             allowEmptyArchive: true
        }

        success {
            echo 'Playwright automation completed successfully.'
        }

        failure {
            echo 'One or more Playwright tests failed.'
        }
    }
}