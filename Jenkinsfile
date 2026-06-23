# =============================================================================
# JENKINSFILE - Complete CI/CD Pipeline
# =============================================================================
#
# Jenkins Pipeline Fundamentals:
# ------------------------------
# A Jenkinsfile defines your CI/CD pipeline as code (Pipeline as Code).
# This is stored in version control alongside your application code.
#
# Benefits:
# - Pipeline is versioned with code
# - Code review for pipeline changes
# - Reproducible builds
# - Single source of truth
#
# Jenkins Architecture:
# ---------------------
#
#   ┌─────────────────────────────────────────────────────────────────┐
#   │                     JENKINS MASTER                               │
#   │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
#   │  │ Scheduler │  │   Queue   │  │  Plugins  │  │ Dashboard │  │
#   │  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
#   └────────────────────────┬────────────────────────────────────────┘
#                            │ Distributes jobs
#              ┌─────────────┼─────────────┐
#              ▼             ▼             ▼
#   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
#   │   Agent 1    │ │   Agent 2    │ │   Agent 3    │
#   │  (Linux)     │ │  (Docker)    │ │  (Windows)   │
#   │  Builds &    │ │  Builds &    │ │  Builds &    │
#   │  Tests       │ │  Deploys     │ │  Tests       │
#   └──────────────┘ └──────────────┘ └──────────────┘
#
# Required Jenkins Plugins:
# - Pipeline
# - Docker Pipeline
# - Git
# - Credentials Binding
# - Blue Ocean (UI)
# - Slack Notification (optional)
# - SonarQube Scanner (optional)
#
# Credentials Setup (Jenkins → Manage Jenkins → Credentials):
# - docker-hub-credentials: Username/Password for Docker Hub
# - kubeconfig: Secret file for Kubernetes access
# - sonar-token: Secret text for SonarQube (optional)
#
# =============================================================================

pipeline {
    // =========================================================================
    // AGENT CONFIGURATION
    // =========================================================================
    // 'any' runs on any available agent
    // In production, you'd specify: agent { label 'docker-agent' }
    agent any

    // =========================================================================
    // ENVIRONMENT VARIABLES
    // =========================================================================
    environment {
        // Application settings
        APP_NAME = 'python-cicd-demo'
        APP_VERSION = "${env.BUILD_NUMBER}"

        // Docker settings
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = "yourusername/${APP_NAME}"
        DOCKER_TAG = "${APP_VERSION}"

        // Kubernetes settings
        K8S_NAMESPACE = 'python-cicd-demo'
        K8S_DEPLOYMENT = 'python-cicd-demo'

        // Credentials (stored securely in Jenkins)
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    }

    // =========================================================================
    // PIPELINE OPTIONS
    // =========================================================================
    options {
        // Timeout entire pipeline after 30 minutes
        timeout(time: 30, unit: 'MINUTES')

        // Keep last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))

        // Add timestamps to console output
        timestamps()

        // Don't allow concurrent builds of same branch
        disableConcurrentBuilds()
    }

    // =========================================================================
    // TRIGGERS
    // =========================================================================
    triggers {
        // Poll SCM every 5 minutes (alternative to webhooks)
        pollSCM('H/5 * * * *')
    }

    // =========================================================================
    // PIPELINE STAGES
    // =========================================================================
    stages {
        // =====================================================================
        // STAGE 1: CHECKOUT CODE
        // =====================================================================
        stage('Checkout Code') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm

                script {
                    // Get git commit info for traceability
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_BRANCH_NAME = sh(
                        script: 'git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Branch: ${env.GIT_BRANCH_NAME}"
                    echo "Commit: ${env.GIT_COMMIT_SHORT}"
                }
            }
        }

        // =====================================================================
        // STAGE 2: INSTALL DEPENDENCIES
        // =====================================================================
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // =====================================================================
        // STAGE 3: RUN UNIT TESTS
        // =====================================================================
        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ \
                        -v \
                        --tb=short \
                        --junitxml=reports/test-results.xml \
                        --cov=app \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=html:reports/coverage-html
                '''
            }
            post {
                always {
                    // Publish test results to Jenkins
                    junit 'reports/test-results.xml'

                    // Archive coverage report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/coverage-html',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        // =====================================================================
        // STAGE 4: CODE QUALITY CHECK
        // =====================================================================
        stage('Code Quality Check') {
            parallel {
                stage('Lint - Flake8') {
                    steps {
                        echo '🔍 Running Flake8 linting...'
                        sh '''
                            . venv/bin/activate
                            flake8 app/ --max-line-length=120 --statistics \
                                --output-file=reports/flake8-report.txt || true
                        '''
                    }
                }
                stage('Security - Bandit') {
                    steps {
                        echo '🔒 Running Bandit security scan...'
                        sh '''
                            . venv/bin/activate
                            bandit -r app/ -f json -o reports/bandit-report.json || true
                        '''
                    }
                }
            }
        }

        // =====================================================================
        // STAGE 5: BUILD DOCKER IMAGE
        // =====================================================================
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    // Build with build args for traceability
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}",
                        "--build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                        "--build-arg GIT_COMMIT=${env.GIT_COMMIT_SHORT} " +
                        "--build-arg VERSION=${DOCKER_TAG} " +
                        "."
                    )
                    // Also tag as latest
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        // =====================================================================
        // STAGE 6: DOCKER IMAGE SCAN
        // =====================================================================
        stage('Docker Image Scan') {
            steps {
                echo '🔐 Scanning Docker image for vulnerabilities...'
                sh '''
                    # Using Trivy for vulnerability scanning
                    # Install: https://aquasecurity.github.io/trivy/
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        --format table \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }

        // =====================================================================
        // STAGE 7: PUSH IMAGE TO DOCKER HUB
        // =====================================================================
        stage('Push to Docker Hub') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'release/*'
                }
            }
            steps {
                echo '📤 Pushing image to Docker Hub...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        // =====================================================================
        // STAGE 8: DEPLOY TO MINIKUBE
        // =====================================================================
        stage('Deploy to Minikube') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo '☸️ Deploying to Kubernetes (Minikube)...'
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            # Update image tag in deployment
                            sed -i 's|IMAGE_TAG|${DOCKER_IMAGE}:${DOCKER_TAG}|g' k8s/deployment.yaml

                            # Apply Kubernetes manifests
                            kubectl apply -f k8s/namespace.yaml
                            kubectl apply -f k8s/configmap.yaml
                            kubectl apply -f k8s/secret.yaml
                            kubectl apply -f k8s/deployment.yaml
                            kubectl apply -f k8s/service.yaml
                            kubectl apply -f k8s/ingress.yaml

                            # Wait for deployment to complete
                            kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                                -n ${K8S_NAMESPACE} \
                                --timeout=120s
                        """
                    }
                }
            }
        }

        // =====================================================================
        // STAGE 9: VERIFY DEPLOYMENT
        // =====================================================================
        stage('Verify Deployment') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo '✅ Verifying deployment...'
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            # Check pod status
                            kubectl get pods -n ${K8S_NAMESPACE} -l app=${APP_NAME}

                            # Get service URL
                            SERVICE_URL=\$(minikube service ${APP_NAME}-service \
                                -n ${K8S_NAMESPACE} --url 2>/dev/null || echo "")

                            if [ -n "\$SERVICE_URL" ]; then
                                # Verify health endpoint
                                echo "Testing health endpoint..."
                                curl -sf \${SERVICE_URL}/health || exit 1

                                # Verify version endpoint
                                echo "Testing version endpoint..."
                                curl -sf \${SERVICE_URL}/version || exit 1

                                echo "✅ Deployment verification successful!"
                            else
                                echo "⚠️ Could not get service URL, checking pod status..."
                                kubectl get pods -n ${K8S_NAMESPACE}
                            fi
                        """
                    }
                }
            }
        }
    }

    // =========================================================================
    // POST-PIPELINE ACTIONS
    // =========================================================================
    post {
        success {
            echo '🎉 Pipeline completed successfully!'
            // Uncomment for Slack notification:
            // slackSend(color: 'good', message: "✅ Build #${BUILD_NUMBER} succeeded for ${APP_NAME}")
        }
        failure {
            echo '❌ Pipeline failed!'
            // slackSend(color: 'danger', message: "❌ Build #${BUILD_NUMBER} failed for ${APP_NAME}")
        }
        always {
            // Clean up Docker images to save disk space
            sh 'docker image prune -f || true'

            // Clean workspace
            cleanWs()
        }
    }
}

// =============================================================================
// JENKINS INSTALLATION & SETUP GUIDE
// =============================================================================
//
// 1. Install Jenkins:
//    docker run -d -p 8080:8080 -p 50000:50000 \
//      -v jenkins_home:/var/jenkins_home \
//      --name jenkins \
//      jenkins/jenkins:lts
//
// 2. Get initial admin password:
//    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
//
// 3. Install suggested plugins + Docker Pipeline, Blue Ocean
//
// 4. Configure credentials:
//    - Docker Hub: Username/Password
//    - Kubeconfig: Secret file
//
// 5. Create pipeline job:
//    - New Item → Pipeline
//    - Pipeline from SCM → Git
//    - Repository URL: your-repo-url
//    - Script Path: Jenkinsfile
//
// =============================================================================

