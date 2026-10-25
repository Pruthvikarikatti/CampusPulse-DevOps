pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Pruthvikarikatti/CampusPulse-DevOps.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"D:\\DevOps\\CampusPulse\\venv\\Scripts\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat '"D:\\DevOps\\CampusPulse\\venv\\Scripts\\python.exe" -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'CampusPulse pipeline completed successfully!'
        }
        failure {
            echo 'CampusPulse pipeline failed. Check the console output.'
        }
    }
}