pipeline {
    agent any

    environment {
        APP_IMAGE = 'online-voting-system'
        COMPOSE_FILE = 'docker-compose.yml'
        WEB_SERVICE = 'web'
        REDIS_SERVICE = 'redis'
    }

    stages {
        stage('Build & Start Services') {
            steps {
                echo 'Building and starting containers...'
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'

                echo 'Waiting for Redis to be ready...'
                sh '''
                for i in {1..30}; do
                    docker-compose exec -T $REDIS_SERVICE redis-cli ping && break || sleep 1
                done
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running pytest inside the web container (excluding Selenium tests)...'
                sh '''
                docker-compose exec -T $WEB_SERVICE /bin/bash -c "
                    export PYTHONPATH=/app &&
                    pytest -v --maxfail=1 --disable-warnings \
                           --ignore=tests/test_ui.py \
                           --junitxml=report.xml
                "
                '''
            }
        }

        stage('Publish Test Report') {
            steps {
                echo 'Publishing pytest results...'
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
            echo 'Cleanup...'
            sh 'docker-compose down || true'
        }
    }
}
