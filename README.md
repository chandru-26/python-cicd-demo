# 🚀 Python CI/CD Demo - Complete DevOps Learning Project

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![Kubernetes](https://img.shields.io/badge/k8s-ready-blue)]()
[![Python](https://img.shields.io/badge/python-3.11-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A complete hands-on DevOps project covering CI/CD, Docker, Jenkins, Kubernetes (Minikube), Git, and TeamCity — from beginner to industry level.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Phase 1: Python Application](#-phase-1-python-application)
- [Phase 2: Git Workflow](#-phase-2-git-workflow)
- [Phase 3: Dockerization](#-phase-3-dockerization)
- [Phase 4: Jenkins CI Pipeline](#-phase-4-jenkins-ci-pipeline)
- [Phase 5: Docker Hub Integration](#-phase-5-docker-hub-integration)
- [Phase 6: Kubernetes Deployment](#-phase-6-kubernetes-deployment)
- [Phase 7: Complete CD Pipeline](#-phase-7-complete-cd-pipeline)
- [Phase 8: TeamCity Implementation](#-phase-8-teamcity-implementation)
- [Phase 9: Production Enhancements](#-phase-9-production-enhancements)
- [DevOps Best Practices](#-devops-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Interview Questions](#-interview-questions)

---

## 🏗 Project Overview

### What This Project Teaches

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE DEVOPS LIFECYCLE                                  │
│                                                                                  │
│  Developer → Git → CI (Jenkins/TeamCity) → Docker → Registry → K8s → Production │
│                                                                                  │
│  ┌──────┐    ┌─────┐    ┌──────────┐    ┌────────┐    ┌─────┐    ┌──────────┐  │
│  │ Code │───▶│ Git │───▶│ CI Server│───▶│ Docker │───▶│ Hub │───▶│   K8s    │  │
│  │      │    │     │    │  Build   │    │ Image  │    │     │    │  Deploy  │  │
│  │      │    │     │    │  Test    │    │        │    │     │    │          │  │
│  └──────┘    └─────┘    └──────────┘    └────────┘    └─────┘    └──────────┘  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
python-cicd-demo/
│
├── app/                          # Application source code
│   ├── __init__.py               # Package initialization
│   ├── app.py                    # Main application (Flask factory)
│   └── routes.py                 # HTTP endpoints (health, version, etc.)
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_app.py              # Pytest test suite
│
├── k8s/                          # Kubernetes manifests
│   ├── namespace.yaml            # Namespace isolation
│   ├── configmap.yaml            # Non-sensitive configuration
│   ├── secret.yaml               # Sensitive data (base64)
│   ├── deployment.yaml           # Pod deployment + HPA
│   ├── service.yaml              # Network exposure
│   └── ingress.yaml              # HTTP routing
│
├── .teamcity/                    # TeamCity configuration
│   └── settings.kts             # Kotlin DSL build config
│
├── Jenkinsfile                   # Jenkins pipeline definition
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml            # Local development setup
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## 🏛 Architecture

### CI/CD Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              CI/CD PIPELINE FLOW                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────────┐  │
│  │   DEV    │     │   GIT    │     │    CI    │     │  DOCKER  │     │  KUBERNETES  │  │
│  │          │────▶│          │────▶│          │────▶│          │────▶│              │  │
│  │  Write   │     │  Push    │     │  Build   │     │  Build   │     │   Deploy     │  │
│  │  Code    │     │  Code    │     │  Test    │     │  Image   │     │   Monitor    │  │
│  │          │     │          │     │  Scan    │     │  Push    │     │   Scale      │  │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────────┘  │
│       │                │                │                │                 │              │
│       ▼                ▼                ▼                ▼                 ▼              │
│  Local Dev         GitHub/         Jenkins/          Docker Hub         Minikube/        │
│  Environment       GitLab          TeamCity          Registry           EKS/GKE         │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KUBERNETES CLUSTER (Minikube)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Namespace: python-cicd-demo                          │ │
│  │                                                                        │ │
│  │  ┌─────────────┐     ┌────────────────────────────────────────────┐   │ │
│  │  │   Ingress   │     │          Deployment (3 replicas)           │   │ │
│  │  │   (NGINX)   │────▶│  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │ │
│  │  └─────────────┘     │  │  Pod 1  │  │  Pod 2  │  │  Pod 3  │   │   │ │
│  │         │             │  │ :5000   │  │ :5000   │  │ :5000   │   │   │ │
│  │         ▼             │  └─────────┘  └─────────┘  └─────────┘   │   │ │
│  │  ┌─────────────┐     └────────────────────────────────────────────┘   │ │
│  │  │   Service   │                                                       │ │
│  │  │  (NodePort) │     ┌──────────────┐     ┌──────────────┐           │ │
│  │  └─────────────┘     │  ConfigMap   │     │    Secret    │           │ │
│  │                       │  (app-config)│     │  (app-secret)│           │ │
│  │                       └──────────────┘     └──────────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌──────────────────────────┐                                               │
│  │   HPA (Auto Scaling)     │                                               │
│  │   Min: 2 / Max: 10       │                                               │
│  │   CPU Target: 70%        │                                               │
│  └──────────────────────────┘                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Phase 1: Python Application

### What You'll Learn
- Flask web framework
- Application factory pattern
- Environment variable configuration
- Health check endpoints
- Structured logging
- Unit testing with pytest

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Development mode
python -m app.app

# Or using Flask CLI
export FLASK_APP=app.app:create_app
flask run --host=0.0.0.0 --port=5000
```

### Run Tests

```bash
# Run all tests
pytest

# Verbose with coverage
pytest -v --cov=app --cov-report=html

# Run specific test
pytest -k "test_health"
```

### Test the Endpoints

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/version
curl http://localhost:5000/ready
curl http://localhost:5000/info
```

### Why This Matters in Industry
- Health check endpoints are REQUIRED for Kubernetes deployments
- The /version endpoint enables deployment verification
- Environment variables follow 12-Factor App methodology
- Structured logging enables centralized log management
- Tests are the foundation of CI/CD pipelines

### Interview Questions
1. What is the 12-Factor App methodology?
2. Why do we need separate health and readiness endpoints?
3. What is the Application Factory pattern in Flask?
4. How do you handle configuration for different environments?
5. What's the difference between unit tests and integration tests?

---

## 🔀 Phase 2: Git Workflow

### Git Basics

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: Python Flask application"

# Connect to remote
git remote add origin https://github.com/yourusername/python-cicd-demo.git
git push -u origin main
```

### Branching Strategy (GitFlow)

```
main (production-ready)
  │
  ├── develop (integration branch)
  │     │
  │     ├── feature/add-health-endpoint
  │     ├── feature/add-docker-support
  │     ├── feature/add-kubernetes-manifests
  │     │
  │     └── release/1.0.0
  │
  └── hotfix/fix-critical-bug
```

### Common Git Commands

```bash
# Create feature branch
git checkout -b feature/add-health-endpoint

# Make changes and commit
git add .
git commit -m "feat: add health check endpoint"

# Push feature branch
git push origin feature/add-health-endpoint

# Create Pull Request (via GitHub/GitLab UI)

# After PR is approved and merged:
git checkout main
git pull origin main

# Create a release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Commit Message Convention

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting (no code change)
refactor: code restructuring
test: adding tests
chore: maintenance tasks
ci: CI/CD changes
```

### Why This Matters in Industry
- Git is the backbone of all CI/CD pipelines
- Branching strategies prevent production incidents
- Pull requests enable code review and quality gates
- Tags enable release versioning and rollbacks
- Commit conventions enable automatic changelog generation

### Interview Questions
1. What is the difference between `git merge` and `git rebase`?
2. Explain GitFlow branching strategy.
3. How do you resolve merge conflicts?
4. What is a Pull Request and why is it important?
5. How do you revert a bad commit in production?

---

## 🐳 Phase 3: Dockerization

### Docker Fundamentals

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCKER ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Docker Engine                           │   │
│  │                                                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │   │
│  │  │ Container1 │  │ Container2 │  │ Container3 │        │   │
│  │  │ (App)      │  │ (Redis)    │  │ (Nginx)    │        │   │
│  │  └────────────┘  └────────────┘  └────────────┘        │   │
│  │       │                │               │                 │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │              Docker Images (Layers)                  │  │   │
│  │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             │  │   │
│  │  │  │ App  │ │Python│ │Debian│ │Nginx │             │  │   │
│  │  │  │Layer │ │Layer │ │Layer │ │Layer │             │  │   │
│  │  │  └──────┘ └──────┘ └──────┘ └──────┘             │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Host Operating System (Linux Kernel)                           │
└─────────────────────────────────────────────────────────────────┘
```

### Build and Run

```bash
# Build the Docker image
docker build -t python-cicd-demo:1.0.0 .

# Run the container
docker run -d -p 5000:5000 --name demo-app python-cicd-demo:1.0.0

# Run with environment variables
docker run -d -p 5000:5000 \
  -e APP_ENV=staging \
  -e APP_VERSION=1.0.0 \
  --name demo-app python-cicd-demo:1.0.0

# Using Docker Compose
docker-compose up -d --build
docker-compose down
```

### Docker Commands Cheatsheet

```bash
# Image Management
docker images                       # List images
docker rmi image_name               # Remove image
docker image prune                  # Remove unused images
docker history image_name           # Show image layers

# Container Management
docker ps                           # Running containers
docker ps -a                        # All containers
docker stop container_name          # Stop container
docker rm container_name            # Remove container
docker logs container_name          # View logs
docker logs -f container_name       # Follow logs
docker exec -it container_name bash # Shell into container
docker inspect container_name       # Detailed info
docker stats                        # Resource usage

# Troubleshooting
docker logs --tail 100 container_name    # Last 100 log lines
docker inspect --format='{{.State.Status}}' container_name
docker events --since '1h'               # Events in last hour
```

### Multi-Stage Build Benefits
1. **Smaller images**: Production image doesn't include build tools
2. **Security**: Fewer packages = smaller attack surface
3. **Speed**: Smaller images deploy faster
4. **Caching**: Better layer caching = faster builds

### Why This Matters in Industry
- Docker ensures consistency across all environments
- "Works on my machine" problem is eliminated
- Containers are the deployment unit for Kubernetes
- Multi-stage builds are a production best practice
- Image scanning prevents deploying vulnerable software

### Interview Questions
1. What is the difference between a Docker image and a container?
2. Explain Docker layer caching and how to optimize it.
3. What is a multi-stage build and why use it?
4. How do you reduce Docker image size?
5. What is the difference between CMD and ENTRYPOINT?
6. Why should containers run as non-root users?

---

## 🔧 Phase 4: Jenkins CI Pipeline

### Jenkins Setup

```bash
# Run Jenkins in Docker
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts

# Get initial password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Pipeline Stages Explained

| Stage | Purpose | What Happens |
|-------|---------|--------------|
| Checkout | Get code | Clone from Git |
| Install Deps | Setup environment | pip install |
| Unit Tests | Verify code works | pytest with coverage |
| Code Quality | Check standards | flake8, bandit |
| Docker Build | Create image | Multi-stage build |
| Image Scan | Security check | Trivy vulnerability scan |
| Push Image | Store artifact | Push to Docker Hub |
| Deploy | Release to K8s | kubectl apply |
| Verify | Confirm deployment | Health check tests |

### Pipeline as Code Benefits
- Version controlled (changes tracked)
- Code review for pipeline changes
- Reproducible across environments
- Shareable across teams
- Testable

### Why This Matters in Industry
- Jenkins is the most widely used CI/CD tool
- Pipeline as Code is an industry standard
- Automated testing catches bugs early (shift-left)
- Automated deployments reduce human error
- Build artifacts provide traceability

### Interview Questions
1. What is the difference between Declarative and Scripted pipeline?
2. Explain Jenkins Master-Agent architecture.
3. How do you handle credentials in Jenkins?
4. What are Jenkins shared libraries?
5. How do you handle parallel stages?
6. What is the difference between `when` and `if` in Jenkinsfile?

---

## 📦 Phase 5: Docker Hub Integration

### Push Image to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag python-cicd-demo:1.0.0 yourusername/python-cicd-demo:1.0.0
docker tag python-cicd-demo:1.0.0 yourusername/python-cicd-demo:latest

# Push to Docker Hub
docker push yourusername/python-cicd-demo:1.0.0
docker push yourusername/python-cicd-demo:latest
```

### Image Tagging Strategy

```
yourusername/python-cicd-demo:1.0.0          # Semantic version
yourusername/python-cicd-demo:latest         # Latest stable
yourusername/python-cicd-demo:main-abc1234   # Branch + commit
yourusername/python-cicd-demo:build-42       # Build number
```

### Why This Matters in Industry
- Docker Hub (or private registries) is where images are stored
- Tags enable version tracking and rollbacks
- Automated push from CI ensures consistent images
- Image scanning in registries adds security layer
- Private registries (ECR, GCR, ACR) for enterprise

---

## ☸️ Phase 6: Kubernetes Deployment

### Prerequisites

```bash
# Install Minikube
# Windows (with chocolatey):
choco install minikube

# Start Minikube
minikube start --driver=docker --memory=4096 --cpus=2

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
```

### Deploy the Application

```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Or apply all at once
kubectl apply -f k8s/
```

### Verify Deployment

```bash
# Check all resources
kubectl get all -n python-cicd-demo

# Check pods
kubectl get pods -n python-cicd-demo -o wide

# Check deployment status
kubectl rollout status deployment/python-cicd-demo -n python-cicd-demo

# Get service URL
minikube service python-cicd-demo-service -n python-cicd-demo --url

# Check logs
kubectl logs -l app=python-cicd-demo -n python-cicd-demo --tail=100

# Describe a pod (for debugging)
kubectl describe pod <pod-name> -n python-cicd-demo
```

### Rolling Updates and Rollbacks

```bash
# Update deployment (change image)
kubectl set image deployment/python-cicd-demo \
  python-cicd-demo=yourusername/python-cicd-demo:2.0.0 \
  -n python-cicd-demo

# Watch the rollout
kubectl rollout status deployment/python-cicd-demo -n python-cicd-demo

# View rollout history
kubectl rollout history deployment/python-cicd-demo -n python-cicd-demo

# Rollback to previous version
kubectl rollout undo deployment/python-cicd-demo -n python-cicd-demo

# Rollback to specific revision
kubectl rollout undo deployment/python-cicd-demo --to-revision=2 -n python-cicd-demo
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment python-cicd-demo --replicas=5 -n python-cicd-demo

# Check HPA
kubectl get hpa -n python-cicd-demo

# Load test to trigger HPA (in another terminal)
# kubectl run load-gen --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://python-cicd-demo-service/health; done"
```

### Troubleshooting Commands

```bash
# Pod not starting?
kubectl describe pod <pod-name> -n python-cicd-demo
kubectl logs <pod-name> -n python-cicd-demo --previous

# Service not routing?
kubectl get endpoints python-cicd-demo-service -n python-cicd-demo

# Shell into a pod
kubectl exec -it <pod-name> -n python-cicd-demo -- /bin/sh

# Check events
kubectl get events -n python-cicd-demo --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n python-cicd-demo
kubectl top nodes
```

### Kubernetes Concepts Summary

| Concept | Purpose | Analogy |
|---------|---------|---------|
| Pod | Smallest deployable unit | A single running process |
| Deployment | Manages pod replicas | A manager ensuring N workers exist |
| Service | Stable network endpoint | A phone number that always reaches someone |
| ConfigMap | Non-sensitive config | A settings file |
| Secret | Sensitive data | A locked safe |
| Namespace | Resource isolation | Different departments in a company |
| Ingress | HTTP routing | A receptionist directing visitors |
| HPA | Auto-scaling | Hiring more workers when busy |

### Why This Matters in Industry
- Kubernetes is the industry standard for container orchestration
- Auto-healing ensures high availability
- Rolling updates enable zero-downtime deployments
- HPA handles traffic spikes automatically
- Declarative config enables GitOps workflows

### Interview Questions
1. What is the difference between a Pod and a Deployment?
2. Explain the difference between liveness and readiness probes.
3. How does a Service discover Pods?
4. What happens when a node fails in Kubernetes?
5. Explain rolling update strategy.
6. How do you debug a CrashLoopBackOff?
7. What is the difference between ConfigMap and Secret?
8. How does HPA work?

---

## 🔄 Phase 7: Complete CD Pipeline

### End-to-End Flow

```
1. Developer pushes code to Git
2. Jenkins detects change (webhook/polling)
3. Pipeline starts automatically
4. Code is checked out
5. Dependencies installed
6. Tests run (fail = pipeline stops)
7. Code quality checked
8. Docker image built
9. Image scanned for vulnerabilities
10. Image pushed to Docker Hub
11. Kubernetes deployment updated
12. Rolling update executes
13. Health checks verify new pods
14. Deployment verified
15. Team notified of success/failure
```

### GitOps Workflow (Advanced)

```
┌──────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────────┐
│Developer │───▶│   Git    │───▶│  CI Pipeline │───▶│ Docker Hub   │
│Push Code │    │(Source)  │    │(Build+Test)  │    │(Store Image) │
└──────────┘    └──────────┘    └──────────────┘    └──────────────┘
                                                           │
                                                           ▼
┌──────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────────┐
│Kubernetes│◀───│  ArgoCD  │◀───│   Git Repo   │◀───│Update Image  │
│ Cluster  │    │(GitOps)  │    │  (K8s YAML)  │    │   Tag        │
└──────────┘    └──────────┘    └──────────────┘    └──────────────┘
```

---

## 🏢 Phase 8: TeamCity Implementation

See `.teamcity/settings.kts` for the complete TeamCity configuration.

### TeamCity Setup

```bash
# Run TeamCity Server
docker run -d --name teamcity-server \
  -v teamcity_data:/data/teamcity_server/datadir \
  -v teamcity_logs:/opt/teamcity/logs \
  -p 8111:8111 \
  jetbrains/teamcity-server

# Run Build Agent
docker run -d --name teamcity-agent \
  -e SERVER_URL="http://host.docker.internal:8111" \
  -v teamcity_agent:/data/teamcity_agent/conf \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jetbrains/teamcity-agent
```

### Key Differences from Jenkins

| Aspect | Jenkins | TeamCity |
|--------|---------|----------|
| Config | Jenkinsfile (Groovy) | Kotlin DSL or UI |
| Agents | Manual setup | Auto-discovery |
| Builds | Sequential stages | Build chains |
| Tests | Plugin-based reporting | Native test history |
| Docker | Needs Docker plugin | Built-in support |

---

## 🏆 Phase 9: Production Enhancements

### 1. Monitoring (Prometheus + Grafana)

```yaml
# Add to your app - prometheus metrics endpoint
# pip install prometheus-flask-instrumentator
```

### 2. Centralized Logging (ELK Stack)

```
App Logs → Filebeat → Logstash → Elasticsearch → Kibana
```

### 3. Secret Management (HashiCorp Vault)

```bash
# Instead of Kubernetes Secrets, use Vault
vault kv put secret/python-cicd-demo SECRET_KEY=my-secret
```

### 4. Infrastructure as Code (Terraform)

```hcl
# Provision Kubernetes cluster
resource "aws_eks_cluster" "main" {
  name     = "production-cluster"
  role_arn = aws_iam_role.cluster.arn
}
```

### 5. Service Mesh (Istio)
- Traffic management
- Security (mTLS)
- Observability

---

## 🛡 DevOps Best Practices

### CI/CD Principles
1. **Automate everything** - No manual deployments
2. **Shift left** - Test early, test often
3. **Small, frequent releases** - Easier to debug
4. **Immutable infrastructure** - Don't modify, replace
5. **Infrastructure as Code** - Everything in Git
6. **Monitor everything** - Observe, alert, respond

### Security (DevSecOps)
1. **Image scanning** - Trivy, Snyk, Anchore
2. **Dependency scanning** - pip-audit, safety
3. **SAST** - Static code analysis (Bandit, SonarQube)
4. **DAST** - Dynamic testing (OWASP ZAP)
5. **Secret management** - Never in code or Git
6. **RBAC** - Least privilege access
7. **Network policies** - Restrict pod communication

### Container Best Practices
1. Use specific image tags (not `:latest` in production)
2. Run as non-root user
3. Use multi-stage builds
4. Scan images for vulnerabilities
5. Keep images small
6. One process per container
7. Use health checks

---

## 🔧 Troubleshooting

### Common Issues and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| Pod CrashLoopBackOff | App crashing | Check logs: `kubectl logs <pod>` |
| ImagePullBackOff | Can't pull image | Check image name/credentials |
| Pending Pod | No resources | Check node resources/quotas |
| Service no endpoints | Label mismatch | Verify selector matches pod labels |
| Ingress not working | Controller missing | `minikube addons enable ingress` |
| Docker build fails | Layer caching issue | `docker build --no-cache` |
| Tests failing in CI | Env difference | Check env vars and dependencies |

---

## 💼 Interview Questions

### CI/CD
1. Explain your CI/CD pipeline from code commit to production.
2. How do you handle rollbacks?
3. What is blue-green deployment vs canary deployment?
4. How do you manage secrets in a pipeline?
5. What metrics do you track for your pipeline?

### Docker
1. Explain Docker networking modes.
2. How do you handle persistent data in containers?
3. What is Docker layer caching?
4. How do you secure a Docker container?
5. Explain multi-stage builds.

### Kubernetes
1. What happens when you run `kubectl apply -f deployment.yaml`?
2. How does service discovery work in Kubernetes?
3. Explain the difference between StatefulSet and Deployment.
4. How do you handle database migrations in Kubernetes?
5. What is a DaemonSet and when would you use one?

### Git
1. How do you handle merge conflicts in a team?
2. Explain your branching strategy.
3. What is `git rebase` and when would you use it?
4. How do you undo the last commit?
5. What are Git hooks?

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [TeamCity Documentation](https://www.jetbrains.com/help/teamcity/)
- [12-Factor App](https://12factor.net/)
- [GitOps Principles](https://opengitops.dev/)

---

## 📄 License

This project is for educational purposes. MIT License.

---

**Built with ❤️ for DevOps learners. Star ⭐ this repo if it helped you!**

