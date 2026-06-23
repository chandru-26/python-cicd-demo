"""
Main Application Entry Point
=============================
This module initializes the Flask application with proper logging,
environment variable support, and configuration management.

DevOps Concepts Demonstrated:
- Environment variable configuration (12-Factor App methodology)
- Structured logging for observability
- Health check endpoints for container orchestration
- Graceful configuration management
"""

import os
import logging
from flask import Flask
from app.routes import register_routes

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# In production, logs are collected by tools like:
# - ELK Stack (Elasticsearch, Logstash, Kibana)
# - Fluentd / Fluent Bit
# - CloudWatch, Stackdriver, Azure Monitor
# Structured logging makes it easier to parse and query logs.

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Application Factory Pattern
    ---------------------------
    This is a best practice in Flask development. It allows:
    - Multiple instances of the app (useful for testing)
    - Different configurations per environment
    - Lazy initialization of extensions

    In DevOps, this pattern supports:
    - Environment-specific deployments (dev, staging, prod)
    - Container-based deployments where config comes from env vars
    - Kubernetes ConfigMaps and Secrets injection
    """
    app = Flask(__name__)

    # ========================================================================
    # ENVIRONMENT VARIABLE CONFIGURATION
    # ========================================================================
    # The 12-Factor App methodology states that configuration should be
    # stored in the environment. This allows the same Docker image to run
    # in different environments (dev, staging, production) with different
    # configurations.
    #
    # In Kubernetes, these come from:
    # - ConfigMaps (non-sensitive data)
    # - Secrets (sensitive data like API keys, passwords)
    # - Environment variables in Pod spec

    app.config['APP_NAME'] = os.environ.get('APP_NAME', 'Python CI/CD Demo')
    app.config['APP_ENV'] = os.environ.get('APP_ENV', 'development')
    app.config['APP_VERSION'] = os.environ.get('APP_VERSION', '1.0.0')
    app.config['APP_PORT'] = int(os.environ.get('APP_PORT', 5000))
    app.config['LOG_LEVEL'] = os.environ.get('LOG_LEVEL', 'INFO')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Set log level from environment
    logging.getLogger().setLevel(app.config['LOG_LEVEL'])

    # Register all routes
    register_routes(app)

    logger.info(f"Application '{app.config['APP_NAME']}' initialized")
    logger.info(f"Environment: {app.config['APP_ENV']}")
    logger.info(f"Version: {app.config['APP_VERSION']}")

    return app


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
# When running directly (not through gunicorn/uwsgi in production)

if __name__ == '__main__':
    app = create_app()
    port = app.config['APP_PORT']
    debug = app.config['APP_ENV'] == 'development'

    logger.info(f"Starting application on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)

