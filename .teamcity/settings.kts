# =============================================================================
# TEAMCITY BUILD CONFIGURATION (Kotlin DSL)
# =============================================================================
#
# TeamCity Architecture:
# ----------------------
#
#   ┌─────────────────────────────────────────────────────────────────────┐
#   │                      TEAMCITY SERVER                                 │
#   │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
#   │  │ Web UI     │  │ REST API   │  │ Build Queue│  │ VCS Roots  │   │
#   │  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
#   │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
#   │  │ Projects   │  │ Build Cfg  │  │ Triggers   │  │ Artifacts  │   │
#   │  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
#   └────────────────────────────┬────────────────────────────────────────┘
#                                │
#              ┌─────────────────┼─────────────────┐
#              ▼                 ▼                 ▼
#   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
#   │   Build Agent 1  │ │   Build Agent 2  │ │   Build Agent 3  │
#   │   (Linux)        │ │   (Docker)       │ │   (Windows)      │
#   │                  │ │                  │ │                  │
#   │ - Python 3.11    │ │ - Docker Engine  │ │ - .NET SDK       │
#   │ - Docker         │ │ - kubectl        │ │ - Python 3.11    │
#   │ - kubectl        │ │ - Helm           │ │ - Docker         │
#   └──────────────────┘ └──────────────────┘ └──────────────────┘
#
# TeamCity vs Jenkins Comparison:
# ===============================
#
# ┌─────────────────────┬────────────────────────┬──────────────────────────┐
# │ Feature             │ Jenkins                │ TeamCity                  │
# ├─────────────────────┼────────────────────────┼──────────────────────────┤
# │ Configuration       │ Jenkinsfile (Groovy)   │ Kotlin DSL / UI          │
# │ Plugins             │ 1800+ (community)      │ 100+ (JetBrains quality) │
# │ Setup Complexity    │ Medium-High            │ Low-Medium               │
# │ Build History       │ Limited by default     │ Built-in, comprehensive  │
# │ VCS Integration     │ Plugin-based           │ Built-in, deep           │
# │ Docker Support      │ Plugin required        │ Built-in                 │
# │ Parallel Builds     │ Pipeline parallel      │ Composite builds         │
# │ Cost                │ Free (open source)     │ Free tier + Commercial   │
# │ Enterprise Support  │ CloudBees (paid)       │ JetBrains (paid)         │
# │ Kubernetes          │ Plugin required        │ Built-in agent support   │
# │ IDE Integration     │ Limited                │ IntelliJ native          │
# │ Build Chain         │ Pipeline stages        │ Snapshot dependencies    │
# │ Personal Builds     │ Not native             │ Built-in                 │
# │ Investigation       │ Manual                 │ Auto-assign failures     │
# │ Test History        │ Plugin needed          │ Built-in flaky test det. │
# └─────────────────────┴────────────────────────┴──────────────────────────┘
#
# When to use Jenkins:
# - Open source requirement
# - Need specific community plugins
# - Budget constraints
# - Already have Jenkins expertise
#
# When to use TeamCity:
# - JetBrains ecosystem (IntelliJ, etc.)
# - Need deep VCS integration
# - Want less plugin management overhead
# - Enterprise features needed out-of-box
# - .NET projects (excellent MSBuild support)
#
# =============================================================================

import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildSteps.*
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.*
import jetbrains.buildServer.configs.kotlin.v2019_2.vcs.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.*

# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

version = "2024.03"

project {
    description = "Python CI/CD Demo - Complete DevOps Pipeline"

    # VCS Root Configuration
    vcsRoot(GitVcsRoot)

    # Build Configurations (Build Chain)
    buildType(BuildAndTest)
    buildType(DockerBuild)
    buildType(DeployToKubernetes)

    # Build Chain Order
    sequential {
        buildType(BuildAndTest)
        buildType(DockerBuild)
        buildType(DeployToKubernetes)
    }
}

# =============================================================================
# VCS ROOT
# =============================================================================

object GitVcsRoot : GitVcsRoot({
    name = "Python CI/CD Demo Repository"
    url = "https://github.com/your-org/python-cicd-demo.git"
    branch = "refs/heads/main"
    branchSpec = "+:refs/heads/*"
    authMethod = password {
        userName = "git"
        password = "credentialsJSON:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
})

# =============================================================================
# BUILD STEP 1: BUILD AND TEST
# =============================================================================

object BuildAndTest : BuildType({
    name = "1. Build and Test"
    description = "Install dependencies, run tests, and check code quality"

    vcs {
        root(GitVcsRoot)
    }

    # Parameters (equivalent to Jenkins environment variables)
    params {
        param("env.APP_VERSION", "%build.number%")
        param("env.PYTHON_VERSION", "3.11")
    }

    steps {
        # Step 1: Install Dependencies
        python {
            name = "Install Dependencies"
            command = file {
                filename = "requirements.txt"
            }
            scriptMode = script {
                content = """
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """.trimIndent()
            }
        }

        # Step 2: Run Unit Tests
        python {
            name = "Run Unit Tests"
            scriptMode = script {
                content = """
                    python -m pytest tests/ \
                        -v \
                        --tb=short \
                        --junitxml=test-results.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html:coverage-html
                """.trimIndent()
            }
        }

        # Step 3: Code Quality - Flake8
        python {
            name = "Code Quality - Flake8"
            scriptMode = script {
                content = """
                    flake8 app/ --max-line-length=120 --statistics --format=default
                """.trimIndent()
            }
        }

        # Step 4: Security Scan - Bandit
        python {
            name = "Security Scan - Bandit"
            scriptMode = script {
                content = """
                    bandit -r app/ -f json -o bandit-report.json || true
                """.trimIndent()
            }
        }
    }

    # Triggers
    triggers {
        vcs {
            branchFilter = "+:*"
            triggerRules = "+:root=${GitVcsRoot.id}:**"
        }
    }

    # Build Features
    features {
        xmlReport {
            reportType = XmlReport.XmlReportType.JUNIT
            rules = "test-results.xml"
        }
        commitStatusPublisher {
            publisher = github {
                githubUrl = "https://api.github.com"
                authType = personalToken {
                    token = "credentialsJSON:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                }
            }
        }
    }

    # Artifact Rules
    artifactRules = """
        test-results.xml
        coverage.xml
        coverage-html/** => coverage-report.zip
        bandit-report.json
    """.trimIndent()
})

# =============================================================================
# BUILD STEP 2: DOCKER BUILD
# =============================================================================

object DockerBuild : BuildType({
    name = "2. Docker Build and Push"
    description = "Build Docker image, scan for vulnerabilities, push to registry"

    vcs {
        root(GitVcsRoot)
    }

    params {
        param("env.DOCKER_REGISTRY", "docker.io")
        param("env.DOCKER_IMAGE", "yourusername/python-cicd-demo")
        param("env.DOCKER_TAG", "%build.number%")
    }

    steps {
        # Step 1: Build Docker Image
        dockerCommand {
            name = "Build Docker Image"
            commandType = build {
                source = file {
                    path = "Dockerfile"
                }
                namesAndTags = "%env.DOCKER_IMAGE%:%env.DOCKER_TAG%"
                commandArgs = "--build-arg VERSION=%env.DOCKER_TAG%"
            }
        }

        # Step 2: Tag as Latest
        script {
            name = "Tag as Latest"
            scriptContent = """
                docker tag %env.DOCKER_IMAGE%:%env.DOCKER_TAG% %env.DOCKER_IMAGE%:latest
            """.trimIndent()
        }

        # Step 3: Scan Image
        script {
            name = "Security Scan with Trivy"
            scriptContent = """
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest image \
                    --severity HIGH,CRITICAL \
                    --exit-code 0 \
                    %env.DOCKER_IMAGE%:%env.DOCKER_TAG%
            """.trimIndent()
        }

        # Step 4: Push to Registry
        dockerCommand {
            name = "Push to Docker Hub"
            commandType = push {
                namesAndTags = """
                    %env.DOCKER_IMAGE%:%env.DOCKER_TAG%
                    %env.DOCKER_IMAGE%:latest
                """.trimIndent()
            }
        }
    }

    # Dependencies
    dependencies {
        snapshot(BuildAndTest) {
            onDependencyFailure = FailureAction.FAIL_TO_START
        }
    }

    # Docker Login Feature
    features {
        dockerSupport {
            loginToRegistry = on {
                dockerRegistryId = "PROJECT_EXT_1"
            }
        }
    }
})

# =============================================================================
# BUILD STEP 3: DEPLOY TO KUBERNETES
# =============================================================================

object DeployToKubernetes : BuildType({
    name = "3. Deploy to Kubernetes"
    description = "Deploy application to Kubernetes cluster"

    vcs {
        root(GitVcsRoot)
    }

    params {
        param("env.K8S_NAMESPACE", "python-cicd-demo")
        param("env.DOCKER_IMAGE", "yourusername/python-cicd-demo")
        param("env.DOCKER_TAG", "%dep.DockerBuild.build.number%")
    }

    steps {
        # Step 1: Update Deployment Manifest
        script {
            name = "Update Image Tag"
            scriptContent = """
                sed -i 's|IMAGE_TAG|%env.DOCKER_IMAGE%:%env.DOCKER_TAG%|g' k8s/deployment.yaml
            """.trimIndent()
        }

        # Step 2: Apply Kubernetes Manifests
        script {
            name = "Deploy to Kubernetes"
            scriptContent = """
                kubectl apply -f k8s/namespace.yaml
                kubectl apply -f k8s/configmap.yaml
                kubectl apply -f k8s/secret.yaml
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/ingress.yaml
            """.trimIndent()
        }

        # Step 3: Wait for Rollout
        script {
            name = "Wait for Deployment"
            scriptContent = """
                kubectl rollout status deployment/python-cicd-demo \
                    -n %env.K8S_NAMESPACE% \
                    --timeout=120s
            """.trimIndent()
        }

        # Step 4: Verify Deployment
        script {
            name = "Verify Deployment"
            scriptContent = """
                echo "=== Pod Status ==="
                kubectl get pods -n %env.K8S_NAMESPACE% -l app=python-cicd-demo
                
                echo "=== Service Status ==="
                kubectl get svc -n %env.K8S_NAMESPACE%
                
                echo "=== Health Check ==="
                SERVICE_URL=$(minikube service python-cicd-demo-service -n %env.K8S_NAMESPACE% --url 2>/dev/null)
                if [ -n "$SERVICE_URL" ]; then
                    curl -sf $SERVICE_URL/health && echo "✅ Health check passed!"
                fi
            """.trimIndent()
        }
    }

    # Dependencies
    dependencies {
        snapshot(DockerBuild) {
            onDependencyFailure = FailureAction.FAIL_TO_START
        }
    }
})

# =============================================================================
# TEAMCITY INSTALLATION GUIDE:
# =============================================================================
#
# Using Docker:
#   docker run -d --name teamcity-server \
#     -v teamcity_data:/data/teamcity_server/datadir \
#     -v teamcity_logs:/opt/teamcity/logs \
#     -p 8111:8111 \
#     jetbrains/teamcity-server
#
# Build Agent:
#   docker run -d --name teamcity-agent \
#     -e SERVER_URL="http://teamcity-server:8111" \
#     -v teamcity_agent:/data/teamcity_agent/conf \
#     -v /var/run/docker.sock:/var/run/docker.sock \
#     jetbrains/teamcity-agent
#
# Access: http://localhost:8111
#
# =============================================================================

