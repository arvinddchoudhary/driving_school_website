pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'arvind09112004/driving_school' // Replace with your Docker Hub repo
        DOCKER_IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' // Replace with your Jenkins Docker Hub credentials ID
        GIT_REPO = 'https://github.com/arvinddchoudhary/driving_school_website.git' // Replace with your GitHub repo URL
        GITHUB_CREDENTIALS_ID = 'github-credentials' // Replace with your Jenkins GitHub credentials ID
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
                    bat """
                    docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%
                    """
                    bat "docker push ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}"
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    // Stop the old container if it's running
                    bat """
                    docker ps -q --filter "name=driving_school" | for /F %i in ('findstr /R /C:"."') do docker stop %i && docker rm %i
                    """

                    // Run the new container
                    bat """
                    docker run -d --name driving_school -p 8000:8000 ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}
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