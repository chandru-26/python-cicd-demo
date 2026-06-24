# 🚀 Jenkins Full CI/CD Setup Guide

Complete the final phase: every `git push` → tests → Docker build → push to Docker Hub → deploy to Kubernetes → verify. **Zero manual steps.**

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ Docker Desktop running
- ✅ Minikube running (`minikube status` → all green)
- ✅ Code pushed to a GitHub repository (so Jenkins can pull it)
- ✅ Docker Hub account (`chandruv12`)

---

## 🔧 PART 1 — Start Jenkins (5 minutes)

### Step 1.1 — Build & start Jenkins container

```powershell
cd C:\devops\python-cicd-demo\jenkins
docker compose up -d --build
```

⏳ **First run takes 3-5 minutes** (downloading Jenkins + installing Docker CLI + kubectl + plugins).

### Step 1.2 — Confirm Jenkins is up

```powershell
docker ps | Select-String jenkins
docker logs jenkins --tail 20
```

You should see: `Jenkins is fully up and running`

### Step 1.3 — Get the initial admin password

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

📋 **Copy this password** — you'll need it next.

### Step 1.4 — Open Jenkins UI

Open in your browser: **http://localhost:8090**

1. Paste the admin password
2. Click **"Install suggested plugins"** (wait ~3 minutes)
3. Create admin user:
   - Username: `admin`
   - Password: `admin123` (or whatever you want)
   - Full name: `Admin`
   - Email: anything
4. Click **"Save and Finish"** → **"Start using Jenkins"**

✅ Jenkins is ready!

---

## 🔐 PART 2 — Add Credentials (5 minutes)

Jenkins needs two credentials: Docker Hub login + kubeconfig for Kubernetes.

### Step 2.1 — Add Docker Hub credentials

1. Jenkins → **Manage Jenkins** → **Credentials**
2. Click **"(global)"** → **"+ Add Credentials"**
3. Fill in:
   - **Kind:** `Username with password`
   - **Username:** `chandruv12`
   - **Password:** Your Docker Hub password (or Access Token from https://hub.docker.com/settings/security)
   - **ID:** `docker-hub-credentials` ← **MUST be exactly this**
   - **Description:** `Docker Hub`
4. Click **Create**

### Step 2.2 — Generate kubeconfig for Jenkins

In PowerShell:
```powershell
cd C:\devops\python-cicd-demo\jenkins
.\prepare-kubeconfig.ps1
```

This creates `jenkins-kubeconfig.yaml` in the `jenkins/` folder.

### Step 2.3 — Upload kubeconfig to Jenkins

1. Jenkins → **Manage Jenkins** → **Credentials** → **(global)** → **Add Credentials**
2. Fill in:
   - **Kind:** `Secret file`
   - **File:** Click "Choose file" → select `C:\devops\python-cicd-demo\jenkins\jenkins-kubeconfig.yaml`
   - **ID:** `kubeconfig` ← **MUST be exactly this**
   - **Description:** `Minikube Kubeconfig`
3. Click **Create**

✅ Credentials done!

---

## 🌱 PART 3 — Create the Pipeline (3 minutes)

### Step 3.1 — Push your code to GitHub (if not already)

```powershell
cd C:\devops\python-cicd-demo
git add .
git commit -m "feat: add Jenkins automation"
git push origin master
```

### Step 3.2 — Create a Pipeline job in Jenkins

1. Jenkins home → **"+ New Item"** (top left)
2. **Item name:** `python-cicd-demo`
3. Select **"Pipeline"** → click **OK**
4. Scroll down to **"Pipeline"** section:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/chandruv12/python-cicd-demo.git` *(your repo URL)*
   - **Credentials:** *(leave blank for public repo, or add GitHub PAT for private)*
   - **Branch:** `*/master` (or `*/main` depending on your default branch)
   - **Script Path:** `Jenkinsfile`
5. Click **Save**

✅ Pipeline created!

---

## ▶️ PART 4 — Run the Pipeline

### Step 4.1 — First manual run

1. On the pipeline page, click **"Build Now"** (left side)
2. Click on the running build (#1) → **"Console Output"**
3. Watch all 6 stages execute live

### Expected output:

```
[Pipeline] Start of Pipeline
[Pipeline] node
[Pipeline] stage: 1. Checkout
  ✓ 📥 Checking out source code...
[Pipeline] stage: 2. Test & Quality
  ✓ 🧪 Running tests... 18 passed
[Pipeline] stage: 3. Build Docker Image
  ✓ 🐳 Built chandruv12/python-cicd-demo:1
[Pipeline] stage: 4. Push to Docker Hub
  ✓ 📤 Pushed to Docker Hub
[Pipeline] stage: 5. Deploy to Minikube
  ✓ ☸️ deployment.apps/python-cicd-demo image updated
  ✓ Waiting for rollout to finish...
  ✓ deployment "python-cicd-demo" successfully rolled out
[Pipeline] stage: 6. Verify
  ✓ 🎉 Deployment successful!
[Pipeline] End of Pipeline
Finished: SUCCESS
```

⏱️ **First run:** ~5-7 minutes (downloads images)
⏱️ **Subsequent runs:** ~2-3 minutes (cached layers)

---

## 🔥 PART 5 — Experience The Full Magic

Now experience the **complete automated flow**:

### Step 5.1 — Make a code change

Open `app/routes.py` and change the home page message:

```python
# Find this in routes.py:
return jsonify({
    "message": "Welcome to Python CI/CD Demo!",
    ...
})

# Change to:
return jsonify({
    "message": "🚀 Updated via Jenkins CI/CD!",
    ...
})
```

### Step 5.2 — Push to Git

```powershell
git add app/routes.py
git commit -m "feat: update home message"
git push origin master
```

### Step 5.3 — Watch the magic ✨

Within 2 minutes (the pollSCM trigger), Jenkins will:
1. ✅ Detect your push
2. ✅ Run all 18 tests
3. ✅ Build a new Docker image (`chandruv12/python-cicd-demo:2`)
4. ✅ Push to Docker Hub
5. ✅ Update Kubernetes deployment (rolling update — zero downtime)
6. ✅ Verify pods are healthy

Watch in Jenkins UI: **http://localhost:8090/job/python-cicd-demo/**

### Step 5.4 — See it live

```powershell
# Start port-forward (in a new window)
Start-Process powershell -ArgumentList "-NoExit","-Command","kubectl port-forward -n python-cicd-demo svc/python-cicd-demo-service 8080:80"

# Test
curl.exe http://localhost:8080/
```

You'll see your updated message! 🎉

---

## 📊 The Complete Flow You Just Built

```
┌──────────────┐    git push     ┌─────────┐
│  Your Code   │ ───────────────►│ GitHub  │
└──────────────┘                 └────┬────┘
                                      │ pollSCM (2 min)
                                      ▼
                                 ┌──────────┐
                                 │ Jenkins  │
                                 │ Pipeline │
                                 └────┬─────┘
                       ┌──────────────┼──────────────┐
                       ▼              ▼              ▼
                  ┌─────────┐   ┌──────────┐   ┌──────────┐
                  │  Tests  │   │  Docker  │   │ K8s      │
                  │ pytest  │   │   Hub    │   │ Rollout  │
                  └─────────┘   └──────────┘   └────┬─────┘
                                                    ▼
                                          ┌──────────────────┐
                                          │ Users see update │
                                          │  (zero downtime) │
                                          └──────────────────┘
```

---

## 🛠️ Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Cannot connect to docker daemon` | Docker socket not mounted | Restart with `docker compose up -d` |
| `Unable to connect to kubernetes` | Kubeconfig points to wrong host | Re-run `prepare-kubeconfig.ps1`, ensure Minikube is running |
| `denied: requested access to repository` | Wrong Docker Hub creds | Re-create `docker-hub-credentials` with Access Token instead of password |
| `kubectl: command not found` | Custom image didn't build | Rebuild: `docker compose up -d --build --force-recreate` |
| `Permission denied /var/run/docker.sock` | Group permissions | We run as root in compose; restart container |
| Pipeline can't find `Jenkinsfile` | Wrong branch/path | Check Pipeline → SCM config — branch should match yours |
| `host.docker.internal` not resolving | Older Docker | Use IP `192.168.49.2` from `minikube ip` instead |

### Useful commands

```powershell
# Jenkins logs
docker logs jenkins -f

# Restart Jenkins
docker compose restart

# Stop Jenkins
docker compose down

# Fully reset (deletes all jobs/credentials!)
docker compose down -v

# Get a fresh admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 🎯 What You Just Accomplished

You now have a **complete production-style CI/CD pipeline**:

| Component | What It Does |
|-----------|--------------|
| **Git** | Stores code + triggers builds on push |
| **Jenkins** | Orchestrates the entire pipeline |
| **Docker** | Builds reproducible application images |
| **Docker Hub** | Distributes images globally |
| **Kubernetes** | Runs the app with auto-healing, rolling updates |
| **Minikube** | Local Kubernetes cluster for development |

This is **exactly** what companies like Netflix, Spotify, Shopify, and Uber use (just at larger scale). You've built the foundation of modern DevOps.

---

## 🏆 Interview Talking Points

After completing this, you can confidently say:

> *"I built a complete CI/CD pipeline using Jenkins as the orchestrator. The pipeline polls Git every 2 minutes, runs unit tests inside ephemeral Python containers for isolation, builds a multi-stage Docker image, pushes versioned tags to Docker Hub using credentials stored in Jenkins' encrypted credentials store, and finally deploys to Kubernetes using `kubectl set image` for zero-downtime rolling updates. The kubeconfig is mounted as a Jenkins Secret File and uses `host.docker.internal` to reach the host's Minikube API server from inside the Jenkins container."*

That's a **senior-level DevOps answer**.

