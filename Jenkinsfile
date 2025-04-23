pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'arvind09112004/driving_school'
        DOCKER_IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        GIT_REPO = 'https://github.com/arvinddchoudhary/driving_school_website.git'
        GITHUB_CREDENTIALS_ID = 'github-credentials'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: "${GITHUB_CREDENTIALS_ID}",
                    url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat """
                        echo|set /p="%DOCKER_PASSWORD%" | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    bat """
                    echo Stopping and removing old container (if exists)...
                    FOR /F %%i IN ('docker ps -q --filter "name=driving_school"') DO (
                        docker stop %%i
                        docker rm %%i
                    )

                    echo Running new container...
                    docker run -d --name driving_school -p 8005:8000 ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
