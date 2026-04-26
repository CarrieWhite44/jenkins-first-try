pipeline {
    agent any

    environment {
        IMAGE_NAME = "tiny-app"
    }

    stages {
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                docker run -d -p 5001:8000 --name test_container $IMAGE_NAME
                sleep 5
                curl -f http://localhost:5001 || exit 1
                docker stop test_container
                docker rm test_container
                '''
            }
        }

        stage('Store Image Locally') {
            steps {
                sh 'docker images | grep $IMAGE_NAME'
            }
        }
    }
}
