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
        docker rm -f test_container || true

        docker run -d -p 5001:8000 --name test_container $IMAGE_NAME

        echo "Waiting for app..."

        for i in $(seq 1 10); do
          curl -f http://localhost:5001 && break
          echo "Not ready yet..."
          sleep 2
        done

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
