# ============================================================================
# QUICK START GUIDE - Python CI/CD Demo
# ============================================================================
# This file contains all commands you just ran, organized for easy reference.
# Run these one at a time in PowerShell from the project folder.
# ============================================================================

# ============================================================================
# STEP 1: SETUP (One-time only)
# ============================================================================

# Navigate to project
cd C:\devops\python-cicd-demo

# Create virtual environment
python -m venv venv

# Activate virtual environment (run this every time you open a new terminal)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# ============================================================================
# STEP 2: RUN THE APP LOCALLY
# ============================================================================

# Start the Flask app
python -m app.app

# Now open your browser and go to:
#   http://localhost:5000          → Home page (JSON)
#   http://localhost:5000/health   → Health check
#   http://localhost:5000/version  → Version info
#   http://localhost:5000/ready    → Readiness check
#   http://localhost:5000/info     → System info

# Press Ctrl+C to stop the app


# ============================================================================
# STEP 3: RUN TESTS
# ============================================================================

# Run all tests
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ -v --cov=app

# Run a specific test
python -m pytest tests/ -k "test_health" -v


# ============================================================================
# STEP 4: CODE QUALITY
# ============================================================================

# Lint check (checks code style)
python -m flake8 app/ --max-line-length=120

# Security scan
python -m bandit -r app/ -ll


# ============================================================================
# STEP 5: DOCKER
# ============================================================================

# Build Docker image
docker build -t python-cicd-demo:1.0.0 .

# Run container
docker run -d -p 5000:5000 --name demo-app python-cicd-demo:1.0.0

# Test it (in browser or PowerShell)
# Browser: http://localhost:5000/health

# View container logs
docker logs demo-app

# Follow logs in real-time
docker logs -f demo-app

# Check container status
docker ps

# Shell into running container
docker exec -it demo-app /bin/sh

# Stop and remove container
docker stop demo-app
docker rm demo-app

# Check image size
docker images python-cicd-demo


# ============================================================================
# STEP 6: GIT
# ============================================================================

# Check status
git status

# View commit history
git log --oneline

# Create a feature branch
git checkout -b feature/my-new-feature

# Make changes, then:
git add .
git commit -m "feat: add my new feature"

# Switch back to main branch
git checkout master

# Merge feature branch
git merge feature/my-new-feature

# Create a release tag
git tag -a v1.1.0 -m "Release v1.1.0"


# ============================================================================
# STEP 7: KUBERNETES (Requires Minikube - install first)
# ============================================================================

# Install Minikube (run in admin PowerShell):
# choco install minikube
# OR download from: https://minikube.sigs.k8s.io/docs/start/

# Start Minikube
minikube start --driver=docker --memory=4096

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Deploy the app (after pushing your image to Docker Hub)
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check everything
kubectl get all -n python-cicd-demo

# Get the URL to access the app
minikube service python-cicd-demo-service -n python-cicd-demo --url

# View pod logs
kubectl logs -l app=python-cicd-demo -n python-cicd-demo

# Cleanup
kubectl delete -f k8s/
minikube stop

