pipeline {
    agent any

    environment {
        APP_IMAGE = 'online-voting-system'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $APP_IMAGE .'
            }
        }

        stage('Run Containers') {
            steps {
                echo 'Starting containers...'
                sh 'docker-compose up -d --build'
                
                // Wait a bit for services to start
                echo 'Waiting for services to become healthy...'
                sh 'sleep 10'

                // Optional: list running containers for debugging
                sh 'docker ps'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
                
                echo 'Running pytest...'
                sh 'pytest -v --maxfail=1 --disable-warnings --ignore=tests/test_ui.py --junitxml=report.xml'
            }
        }

        stage('Publish Test Report') {
            steps {
                echo 'Publishing test report...'
                junit 'report.xml'
            }
        }

        stage('Tear Down') {
            steps {
                echo 'Stopping containers...'
                sh 'docker-compose down'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up just in case...'
            sh 'docker-compose down || true'
        }
    }
}
