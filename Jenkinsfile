pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "fintechx_project"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/iarlenaquiles/FinTechX.git'
            }
        }

        stage('Build & Deploy') {
            steps {
                sh '''
                    docker compose down --remove-orphans || true
                    docker compose build
                    docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deploy concluído com sucesso com Docker Compose!'
        }
        failure {
            echo '❌ Falha no deploy com Docker Compose.'
        }
    }
}