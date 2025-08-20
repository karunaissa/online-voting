pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t online-voting-system .'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker compose up -d'
                // small delay to ensure services are up
                sh 'sleep 5'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest -v --maxfail=1 --disable-warnings --ignore=tests/test_ui.py --junitxml=report.xml'
            }
        }

        stage('Publish Test Report') {
            steps {
                junit 'report.xml'
            }
        }

        stage('Tear Down') {
            steps {
                sh 'docker compose down'
            }
        }
    }
}
