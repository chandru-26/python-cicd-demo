# =============================================================================
# DOCKERFILE - Python CI/CD Demo Application
# =============================================================================
#
# Docker Fundamentals:
# --------------------
# A Dockerfile is a blueprint for creating Docker images.
# Each instruction creates a layer in the image.
# Docker uses a layered filesystem (Union FS) for efficiency.
#
# Multi-Stage Build:
# ------------------
# We use multi-stage builds to:
# 1. Keep the final image small (security + faster deployments)
# 2. Separate build dependencies from runtime dependencies
# 3. Reduce attack surface in production
#
# Image Optimization Tips:
# - Use slim/alpine base images
# - Minimize layers (combine RUN commands)
# - Use .dockerignore to exclude unnecessary files
# - Order instructions from least to most frequently changed
# - Leverage build cache effectively
#
# =============================================================================

# =============================================================================
# STAGE 1: Builder Stage
# =============================================================================
# Purpose: Install dependencies and run tests
# This stage is discarded in the final image

FROM python:3.11-slim as builder

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents .pyc files (smaller image)
# PYTHONUNBUFFERED: Ensures logs appear in real-time (important for Docker)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /build

# Copy requirements first (Docker layer caching optimization)
# If requirements.txt hasn't changed, Docker reuses the cached layer
COPY requirements.txt .

# Install dependencies
RUN pip install --prefix=/install -r requirements.txt

# Copy application code
COPY . .

# Run tests during build (shift-left testing)
RUN pip install -r requirements.txt && \
    python -m pytest tests/ -v --tb=short

# =============================================================================
# STAGE 2: Production Stage
# =============================================================================
# Purpose: Minimal image with only runtime dependencies
# Result: Much smaller image (~150MB vs ~500MB+)

FROM python:3.11-slim as production

# Labels for image metadata (OCI standard)
# These are queryable with `docker inspect`
LABEL maintainer="devops-team@company.com" \
      version="1.0.0" \
      description="Python CI/CD Demo Application" \
      org.opencontainers.image.source="https://github.com/your-org/python-cicd-demo"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    APP_PORT=5000

# Create non-root user (Security Best Practice)
# Running as root in containers is a security risk
# If container is compromised, attacker has limited privileges
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (documentation - doesn't actually publish the port)
EXPOSE 5000

# Health check - Docker will monitor container health
# Kubernetes has its own probes, but this works for Docker Compose
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run with gunicorn (production-grade WSGI server)
# - Workers: typically 2*CPU + 1
# - Bind to 0.0.0.0 to accept external connections
# - Timeout: prevent hanging requests
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "app.app:create_app()"]

# =============================================================================
# BUILD AND RUN COMMANDS:
# =============================================================================
#
# Build the image:
#   docker build -t python-cicd-demo:1.0.0 .
#   docker build -t python-cicd-demo:latest .
#   docker build --no-cache -t python-cicd-demo:1.0.0 .  # Force rebuild
#
# Run the container:
#   docker run -d -p 5000:5000 --name demo-app python-cicd-demo:1.0.0
#   docker run -d -p 5000:5000 -e APP_ENV=staging python-cicd-demo:1.0.0
#   docker run -d -p 5000:5000 --env-file .env python-cicd-demo:1.0.0
#
# Troubleshooting:
#   docker logs demo-app                    # View logs
#   docker logs -f demo-app                 # Follow logs
#   docker exec -it demo-app /bin/bash      # Shell into container
#   docker inspect demo-app                 # Inspect container
#   docker stats demo-app                   # Resource usage
#   docker history python-cicd-demo:1.0.0   # Image layer history
#
# Push to Docker Hub:
#   docker login
#   docker tag python-cicd-demo:1.0.0 yourusername/python-cicd-demo:1.0.0
#   docker push yourusername/python-cicd-demo:1.0.0
#
# =============================================================================

