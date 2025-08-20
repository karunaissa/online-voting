pipeline {
    agent any

    environment {
        APP_IMAGE = 'online-voting-system'
        COMPOSE_FILE = 'docker-compose.yml'
        WEB_SERVICE = 'web'
        REDIS_SERVICE = 'redis'
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
                for i in {1..30}; do
                    docker-compose exec -T $REDIS_SERVICE redis-cli ping &>/dev/null && break || sleep 1
                done

                for i in {1..30}; do
                    docker-compose exec -T $WEB_SERVICE curl -s http://localhost:5000/ &>/dev/null && break || sleep 1
                done

                echo "Services are ready!"
                docker ps
                """
            }
        }

        stage('Run Tests with Logs') {
            steps {
                echo 'Streaming Flask and Redis logs while running tests...'
                sh """
                # Stream logs in background
                docker-compose logs -f $WEB_SERVICE > flask.log 2>&1 &
                docker-compose logs -f $REDIS_SERVICE > redis.log 2>&1 &

                # Run tests inside the Flask container
                docker-compose exec -T $WEB_SERVICE /bin/bash -c '
                    export PYTHONPATH=/app &&
                    pytest -v --maxfail=1 --disable-warnings --ignore=tests/test_ui.py --junitxml=report.xml
                '

                # Kill background log tailing
                pkill -f "docker-compose logs -f"
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
