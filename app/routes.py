"""
Application Routes
==================
This module defines all HTTP endpoints for the application.

DevOps-Critical Endpoints:
- /health  → Used by Kubernetes liveness/readiness probes
- /version → Used for deployment verification and rollback decisions
- /ready   → Used by Kubernetes readiness probe (can include dependency checks)

Why These Endpoints Matter in Production:
------------------------------------------
1. Health Check (/health):
   - Kubernetes uses this to determine if a pod is alive
   - Load balancers use this to route traffic
   - Monitoring systems use this for alerting

2. Version (/version):
   - Helps verify which version is deployed
   - Critical for canary deployments and blue-green deployments
   - Used in CI/CD pipeline verification stages

3. Readiness (/ready):
   - Kubernetes uses this to know when a pod can accept traffic
   - Different from health: a pod can be alive but not ready
   - Example: pod is alive but database connection isn't established yet
"""

import os
import logging
import platform
from datetime import datetime
from flask import jsonify, current_app

logger = logging.getLogger(__name__)


def register_routes(app):
    """Register all application routes."""

    # ========================================================================
    # HOME PAGE
    # ========================================================================
    @app.route('/')
    def home():
        """
        Home page - Returns application information.
        In a real application, this might serve the frontend or API docs.
        """
        logger.info("Home page accessed")
        return jsonify({
            'application': current_app.config['APP_NAME'],
            'environment': current_app.config['APP_ENV'],
            'version': current_app.config['APP_VERSION'],
            'message': 'Welcome to the Python CI/CD Demo Application!',
            'documentation': '/docs',
            'health_check': '/health',
            'endpoints': {
                'home': '/',
                'health': '/health',
                'ready': '/ready',
                'version': '/version',
                'info': '/info'
            }
        })

    # ========================================================================
    # HEALTH CHECK ENDPOINT
    # ========================================================================
    @app.route('/health')
    def health():
        """
        Health Check Endpoint
        ---------------------
        Used by:
        - Kubernetes livenessProbe
        - Docker HEALTHCHECK
        - Load Balancers
        - Monitoring Systems (Prometheus, Nagios, etc.)

        Kubernetes Configuration Example:
            livenessProbe:
              httpGet:
                path: /health
                port: 5000
              initialDelaySeconds: 10
              periodSeconds: 5
              failureThreshold: 3

        If this endpoint returns non-200, Kubernetes will restart the pod.
        """
        logger.debug("Health check requested")
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': 'ok'
        }), 200

    # ========================================================================
    # READINESS ENDPOINT
    # ========================================================================
    @app.route('/ready')
    def ready():
        """
        Readiness Probe Endpoint
        ------------------------
        Indicates whether the application is ready to serve traffic.

        In production, this would check:
        - Database connectivity
        - Cache availability (Redis)
        - External service dependencies
        - Message queue connectivity

        Kubernetes Configuration Example:
            readinessProbe:
              httpGet:
                path: /ready
                port: 5000
              initialDelaySeconds: 5
              periodSeconds: 3
              failureThreshold: 3

        If this returns non-200, Kubernetes removes the pod from the
        Service's endpoints (no traffic routed to it).
        """
        # In a real app, check dependencies here
        checks = {
            'application': True,
            # 'database': check_database(),
            # 'cache': check_redis(),
            # 'external_api': check_external_service(),
        }

        all_ready = all(checks.values())
        status_code = 200 if all_ready else 503

        return jsonify({
            'ready': all_ready,
            'checks': checks,
            'timestamp': datetime.utcnow().isoformat()
        }), status_code

    # ========================================================================
    # VERSION ENDPOINT
    # ========================================================================
    @app.route('/version')
    def version():
        """
        Version Endpoint
        ----------------
        Critical for:
        - Deployment verification in CI/CD pipelines
        - Rollback decisions
        - Canary deployment validation
        - Blue-green deployment switching

        The version is injected via environment variable during deployment.
        In Kubernetes, this comes from the image tag or a ConfigMap.
        """
        logger.info("Version info requested")
        return jsonify({
            'version': current_app.config['APP_VERSION'],
            'environment': current_app.config['APP_ENV'],
            'python_version': platform.python_version(),
            'build_date': os.environ.get('BUILD_DATE', 'unknown'),
            'git_commit': os.environ.get('GIT_COMMIT', 'unknown'),
            'git_branch': os.environ.get('GIT_BRANCH', 'unknown')
        })

    # ========================================================================
    # APPLICATION INFO ENDPOINT
    # ========================================================================
    @app.route('/info')
    def info():
        """
        Detailed application information.
        Useful for debugging in non-production environments.
        """
        logger.info("Application info requested")
        return jsonify({
            'app_name': current_app.config['APP_NAME'],
            'environment': current_app.config['APP_ENV'],
            'version': current_app.config['APP_VERSION'],
            'hostname': platform.node(),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'timestamp': datetime.utcnow().isoformat()
        })

    # ========================================================================
    # ERROR HANDLERS
    # ========================================================================
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        logger.warning(f"404 error: {error}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"500 error: {error}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

