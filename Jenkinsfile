pipeline {
    agent any

    environment {
        APP_IMAGE = 'online-voting-system'
        COMPOSE_FILE = 'docker-compose.yml'
        WEB_CONTAINER = 'online-voting-system-web-1'
        REDIS_CONTAINER = 'online-voting-system-redis-1'
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

                // Wait for services to be healthy
                echo 'Waiting for Redis and Flask to be ready...'
                sh """
                # Wait up to 30 seconds for Redis
                for i in {1..30}; do
                    docker exec $REDIS_CONTAINER redis-cli ping &>/dev/null && break || sleep 1
                done

                # Wait up to 30 seconds for Flask
                for i in {1..30}; do
                    docker exec $WEB_CONTAINER curl -s http://localhost:5000/ &>/dev/null && break || sleep 1
                done

                echo "Services are ready!"
                docker ps
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests inside the Flask container...'
                sh """
                docker exec -i $WEB_CONTAINER /bin/bash -c '
                    python3 -m venv venv &&
                    . venv/bin/activate &&
                    pip install --upgrade pip &&
                    pip install -r requirements.txt &&
                    pytest -v --maxfail=1 --disable-warnings --ignore=tests/test_ui.py --junitxml=report.xml
                '
                """
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
