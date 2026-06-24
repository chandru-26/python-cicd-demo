// =============================================================================
// JENKINSFILE - Complete CI/CD Pipeline (Production-Ready)
// =============================================================================
// Pipeline: checkout → test → build → push → deploy → verify
// Image:    chandruv12/python-cicd-demo:<BUILD_NUMBER>
// Target:   Minikube namespace "python-cicd-demo"
//
// Required Jenkins credentials:
//   - docker-hub-credentials  (Username with password — Docker Hub)
//   - kubeconfig              (Secret file — your minikube kubeconfig)
// =============================================================================

pipeline {
    agent any

    environment {
        APP_NAME        = 'python-cicd-demo'
        DOCKER_USERNAME = 'chandruv12'
        DOCKER_IMAGE    = "${DOCKER_USERNAME}/${APP_NAME}"
        DOCKER_TAG      = "${env.BUILD_NUMBER}"
        K8S_NAMESPACE   = 'python-cicd-demo'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('1. Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Commit: ${env.GIT_COMMIT_SHORT}"
                }
            }
        }

        stage('2. Test & Quality') {
            steps {
                echo '🧪 Running tests in Python container...'
                sh '''
                    docker run --rm -v "$PWD":/app -w /app python:3.11-slim sh -c "
                        pip install --no-cache-dir -r requirements.txt &&
                        pip install --no-cache-dir flake8 bandit &&
                        mkdir -p reports &&
                        python -m pytest tests/ -v --junitxml=reports/test-results.xml &&
                        flake8 app/ --max-line-length=120 || true &&
                        bandit -r app/ -ll || true
                    "
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
                }
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo "🐳 Building ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh '''
                    docker build \
                        -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        -t ${DOCKER_IMAGE}:latest \
                        .
                '''
            }
        }

        stage('4. Push to Docker Hub') {
            steps {
                echo "📤 Pushing image to Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('5. Deploy to Minikube') {
            steps {
                echo "☸️  Deploying to Kubernetes..."
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KCFG')]) {
                    sh '''
                        export KUBECONFIG=$KCFG
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/secret.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl set image deployment/${APP_NAME} \
                            ${APP_NAME}=${DOCKER_IMAGE}:${DOCKER_TAG} \
                            -n ${K8S_NAMESPACE}
                        kubectl rollout status deployment/${APP_NAME} \
                            -n ${K8S_NAMESPACE} --timeout=180s
                    '''
                }
            }
        }

        stage('6. Verify') {
            steps {
                echo "✅ Verifying deployment..."
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KCFG')]) {
                    sh '''
                        export KUBECONFIG=$KCFG
                        kubectl get pods -n ${K8S_NAMESPACE}
                        kubectl get deploy ${APP_NAME} -n ${K8S_NAMESPACE}
                        echo "🎉 Deployment successful!"
                    '''
                }
            }
        }
    }

    post {
        success { echo "🎉 Build #${BUILD_NUMBER} succeeded — ${DOCKER_IMAGE}:${DOCKER_TAG}" }
        failure { echo "❌ Build #${BUILD_NUMBER} failed" }
        always  { sh 'docker image prune -f || true' }
    }
}
