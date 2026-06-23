# ============================================================================
# NEXT STEPS GUIDE - Detailed Instructions for Beginners
# ============================================================================
# You have already completed: App setup, Tests, Docker build, Git init
# Now follow these steps one by one.
# ============================================================================


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  STEP A: INSTALL MINIKUBE & DEPLOY TO KUBERNETES                         ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# --------------------------------------------------------------------------
# A1. INSTALL MINIKUBE
# --------------------------------------------------------------------------
# 
# WHAT IS MINIKUBE?
# Minikube runs a mini Kubernetes cluster on your laptop.
# It's like having a tiny server farm on your computer for practice.
#
# OPTION 1: Using Chocolatey (easiest)
# Open PowerShell AS ADMINISTRATOR (right-click → Run as Administrator)

choco install minikube -y

# OPTION 2: Direct download (if you don't have chocolatey)
# Go to: https://minikube.sigs.k8s.io/docs/start/
# Download the Windows installer (.exe)
# Run the installer, click Next through everything

# VERIFY INSTALLATION (open a NEW PowerShell window after install):
minikube version

# --------------------------------------------------------------------------
# A2. START MINIKUBE
# --------------------------------------------------------------------------
# This creates a virtual mini-cluster on your machine.
# Make sure Docker Desktop is RUNNING first!

minikube start --driver=docker --memory=4096 --cpus=2

# Wait 2-5 minutes. You'll see output like:
# ✅ Done! kubectl is now configured to use "minikube" cluster

# VERIFY it's running:
minikube status
kubectl cluster-info

# --------------------------------------------------------------------------
# A3. ENABLE REQUIRED ADDONS
# --------------------------------------------------------------------------

minikube addons enable ingress
minikube addons enable metrics-server

# --------------------------------------------------------------------------
# A4. LOAD YOUR DOCKER IMAGE INTO MINIKUBE
# --------------------------------------------------------------------------
# Minikube has its own Docker daemon. You need to load your image into it.
# (This avoids needing Docker Hub for local testing)

# First, build the image if you haven't:
cd C:\devops\python-cicd-demo
docker build -t python-cicd-demo:1.0.0 .

# Load it into Minikube:
minikube image load python-cicd-demo:1.0.0

# Verify it's there:
minikube image list | Select-String "python-cicd"

# --------------------------------------------------------------------------
# A5. UPDATE DEPLOYMENT YAML FOR LOCAL TESTING
# --------------------------------------------------------------------------
# We need to change "IMAGE_TAG" in deployment.yaml to our actual image.
# 
# Open k8s/deployment.yaml and change this line:
#   image: IMAGE_TAG
# To:
#   image: python-cicd-demo:1.0.0
#
# Also change imagePullPolicy from "Always" to "Never" (since image is local)
#   imagePullPolicy: Never

# --------------------------------------------------------------------------
# A6. DEPLOY TO KUBERNETES
# --------------------------------------------------------------------------

# Apply all Kubernetes files (ORDER MATTERS):
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# --------------------------------------------------------------------------
# A7. CHECK YOUR DEPLOYMENT
# --------------------------------------------------------------------------

# See all resources:
kubectl get all -n python-cicd-demo

# Check if pods are running (wait until STATUS = Running):
kubectl get pods -n python-cicd-demo

# If pods show "ContainerCreating" - wait 30 seconds and check again
# If pods show "CrashLoopBackOff" - check logs (see troubleshooting below)

# --------------------------------------------------------------------------
# A8. ACCESS YOUR APP IN KUBERNETES
# --------------------------------------------------------------------------

# Get the URL to access your app:
minikube service python-cicd-demo-service -n python-cicd-demo --url

# This will print a URL like: http://192.168.49.2:30080
# Open that URL in your browser!
# Try: http://<that-url>/health
# Try: http://<that-url>/version

# --------------------------------------------------------------------------
# A9. KUBERNETES TROUBLESHOOTING
# --------------------------------------------------------------------------

# If pods aren't starting, check what's wrong:
kubectl describe pod -l app=python-cicd-demo -n python-cicd-demo

# Check container logs:
kubectl logs -l app=python-cicd-demo -n python-cicd-demo

# Check events (shows errors):
kubectl get events -n python-cicd-demo --sort-by='.lastTimestamp'

# Shell into a running pod:
kubectl exec -it <pod-name> -n python-cicd-demo -- /bin/sh

# --------------------------------------------------------------------------
# A10. CLEANUP KUBERNETES
# --------------------------------------------------------------------------

# Delete all resources:
kubectl delete -f k8s/

# Stop Minikube (saves battery/RAM):
minikube stop

# Delete Minikube completely (if you want to start fresh):
minikube delete


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  STEP B: PUSH TO GITHUB                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# --------------------------------------------------------------------------
# B1. CREATE A GITHUB ACCOUNT (skip if you already have one)
# --------------------------------------------------------------------------
# Go to: https://github.com
# Click "Sign Up" → Follow the steps
# Verify your email

# --------------------------------------------------------------------------
# B2. CREATE A NEW REPOSITORY ON GITHUB
# --------------------------------------------------------------------------
# 1. Log into GitHub
# 2. Click the "+" icon (top-right corner) → "New repository"
# 3. Fill in:
#    - Repository name: python-cicd-demo
#    - Description: Complete DevOps learning project
#    - Select: Public (so others can see) or Private (only you)
#    - Do NOT check "Add a README" (we already have one)
#    - Do NOT check "Add .gitignore" (we already have one)
# 4. Click "Create repository"
#
# GitHub will show you a page with commands. Copy the URL shown.
# It looks like: https://github.com/YOUR-USERNAME/python-cicd-demo.git

# --------------------------------------------------------------------------
# B3. CONNECT YOUR LOCAL PROJECT TO GITHUB
# --------------------------------------------------------------------------

cd C:\devops\python-cicd-demo

# Replace YOUR-USERNAME with your actual GitHub username:
git remote add origin https://github.com/YOUR-USERNAME/python-cicd-demo.git

# Verify the remote was added:
git remote -v

# --------------------------------------------------------------------------
# B4. PUSH YOUR CODE TO GITHUB
# --------------------------------------------------------------------------

# Push your code (first time - sets up tracking):
git push -u origin master

# It will ask for your GitHub credentials.
# 
# ⚠️ IMPORTANT: GitHub no longer accepts passwords!
# You need a Personal Access Token:
#
# 1. Go to: https://github.com/settings/tokens
# 2. Click "Generate new token (classic)"
# 3. Give it a name: "my-laptop"
# 4. Select scopes: check "repo" (full control)
# 5. Click "Generate token"
# 6. COPY THE TOKEN (you won't see it again!)
#
# When git asks for password, paste the TOKEN (not your password)
#
# Username: your-github-username
# Password: ghp_xxxxxxxxxxxxxxxxxxxx (the token)

# Push the tag too:
git push origin v1.0.0

# --------------------------------------------------------------------------
# B5. VERIFY ON GITHUB
# --------------------------------------------------------------------------
# 1. Go to: https://github.com/YOUR-USERNAME/python-cicd-demo
# 2. You should see all your files there!
# 3. Click on README.md - it renders beautifully with all the diagrams

# --------------------------------------------------------------------------
# B6. FUTURE WORKFLOW (after initial push)
# --------------------------------------------------------------------------

# Make changes to any file, then:
git add .
git commit -m "feat: describe what you changed"
git push

# That's it! Changes appear on GitHub.


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  STEP C: PUSH TO DOCKER HUB                                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# --------------------------------------------------------------------------
# C1. CREATE A DOCKER HUB ACCOUNT
# --------------------------------------------------------------------------
# Go to: https://hub.docker.com
# Click "Sign Up" (free account)
# Remember your username!

# --------------------------------------------------------------------------
# C2. LOGIN TO DOCKER HUB FROM TERMINAL
# --------------------------------------------------------------------------

docker login

# Enter your Docker Hub username and password when prompted.
# You'll see: "Login Succeeded"

# --------------------------------------------------------------------------
# C3. TAG YOUR IMAGE FOR DOCKER HUB
# --------------------------------------------------------------------------
# Docker Hub images must be named: YOUR-DOCKERHUB-USERNAME/image-name:tag
#
# Replace "yourusername" with your actual Docker Hub username:

docker tag python-cicd-demo:1.0.0 yourusername/python-cicd-demo:1.0.0
docker tag python-cicd-demo:1.0.0 yourusername/python-cicd-demo:latest

# Verify tags were created:
docker images | Select-String "python-cicd-demo"

# --------------------------------------------------------------------------
# C4. PUSH TO DOCKER HUB
# --------------------------------------------------------------------------

docker push yourusername/python-cicd-demo:1.0.0
docker push yourusername/python-cicd-demo:latest

# Wait for upload... (first time is slower, ~60MB)
# You'll see layer-by-layer upload progress.

# --------------------------------------------------------------------------
# C5. VERIFY ON DOCKER HUB
# --------------------------------------------------------------------------
# 1. Go to: https://hub.docker.com
# 2. Click on your profile → "Repositories"
# 3. You'll see "python-cicd-demo" listed!
# 4. Anyone can now pull your image with:
#    docker pull yourusername/python-cicd-demo:1.0.0

# --------------------------------------------------------------------------
# C6. WHY THIS MATTERS
# --------------------------------------------------------------------------
# Now that your image is on Docker Hub:
# - Kubernetes can pull it from anywhere in the world
# - Your CI/CD pipeline (Jenkins) pushes here automatically
# - Other team members can pull and run your exact same app
# - It's like "npm publish" but for Docker containers


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  COMMON PROBLEMS & SOLUTIONS                                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# --------------------------------------------------------------------------
# PROBLEM: "choco is not recognized"
# SOLUTION: Install Chocolatey first:
#   Open PowerShell as Admin and run:
#   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# PROBLEM: "minikube start" hangs or fails
# SOLUTION: 
#   1. Make sure Docker Desktop is running
#   2. Try: minikube delete; minikube start --driver=docker
#   3. If still fails: minikube start --driver=hyperv (needs Hyper-V enabled)
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# PROBLEM: "git push" asks for password and rejects it
# SOLUTION: Use a Personal Access Token (see step B4 above)
#   GitHub killed password authentication in 2021.
#   You MUST use a token instead of your password.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# PROBLEM: "docker push" says "denied: requested access to the resource is denied"
# SOLUTION: 
#   1. Make sure you ran "docker login" first
#   2. Make sure image is tagged with YOUR username: yourusername/python-cicd-demo
#   3. The tag must match your Docker Hub username exactly
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# PROBLEM: Kubernetes pods stuck in "ImagePullBackOff"
# SOLUTION:
#   This means K8s can't find the Docker image.
#   For local testing: use "minikube image load" + imagePullPolicy: Never
#   For real deployment: push image to Docker Hub first
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# PROBLEM: Kubernetes pods in "CrashLoopBackOff"
# SOLUTION:
#   The app is crashing. Check why:
#   kubectl logs <pod-name> -n python-cicd-demo
#   kubectl describe pod <pod-name> -n python-cicd-demo
# --------------------------------------------------------------------------

