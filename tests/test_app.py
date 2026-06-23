"""
Unit Tests for Python CI/CD Demo Application
=============================================

Why Unit Tests Matter in DevOps:
- They run automatically in CI/CD pipelines
- They catch bugs before code reaches production
- They provide confidence for automated deployments
- Failed tests block the pipeline (shift-left testing)

Testing Pyramid:
    /    E2E Tests     \    ← Slow, expensive, few
   /  Integration Tests  \   ← Medium speed, some
  /     Unit Tests         \  ← Fast, cheap, many

In CI/CD pipelines:
- Unit tests run on every commit
- Integration tests run on merge to main
- E2E tests run before production deployment

Running Tests:
    pytest                          # Run all tests
    pytest -v                       # Verbose output
    pytest --cov=app                # With coverage report
    pytest --cov=app --cov-report=html  # HTML coverage report
    pytest -x                       # Stop on first failure
    pytest -k "test_health"         # Run specific tests
"""

import pytest
import json
from app.app import create_app


# ============================================================================
# FIXTURES
# ============================================================================
# Fixtures provide reusable test setup. They follow the Arrange-Act-Assert pattern.

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client.

    The test client allows us to make HTTP requests to our app
    without running a real server. This makes tests fast and isolated.
    """
    return app.test_client()


# ============================================================================
# HOME PAGE TESTS
# ============================================================================

class TestHomePage:
    """Tests for the home page endpoint."""

    def test_home_returns_200(self, client):
        """Test that home page returns HTTP 200 OK."""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_returns_json(self, client):
        """Test that home page returns JSON content type."""
        response = client.get('/')
        assert response.content_type == 'application/json'

    def test_home_contains_app_name(self, client):
        """Test that home page contains application name."""
        response = client.get('/')
        data = json.loads(response.data)
        assert 'application' in data
        assert data['application'] == 'Python CI/CD Demo'

    def test_home_contains_endpoints(self, client):
        """Test that home page lists available endpoints."""
        response = client.get('/')
        data = json.loads(response.data)
        assert 'endpoints' in data
        assert '/health' in data['endpoints'].values()


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

class TestHealthCheck:
    """
    Tests for the health check endpoint.

    These tests verify that Kubernetes probes will work correctly.
    A failing health check in production means pods get restarted!
    """

    def test_health_returns_200(self, client):
        """Test that health endpoint returns HTTP 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Test that health endpoint reports healthy status."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_health_contains_timestamp(self, client):
        """Test that health response includes timestamp."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'timestamp' in data


# ============================================================================
# READINESS TESTS
# ============================================================================

class TestReadiness:
    """Tests for the readiness probe endpoint."""

    def test_ready_returns_200(self, client):
        """Test that readiness endpoint returns HTTP 200 OK."""
        response = client.get('/ready')
        assert response.status_code == 200

    def test_ready_returns_ready_status(self, client):
        """Test that readiness endpoint reports ready."""
        response = client.get('/ready')
        data = json.loads(response.data)
        assert data['ready'] is True

    def test_ready_contains_checks(self, client):
        """Test that readiness response includes dependency checks."""
        response = client.get('/ready')
        data = json.loads(response.data)
        assert 'checks' in data


# ============================================================================
# VERSION ENDPOINT TESTS
# ============================================================================

class TestVersion:
    """
    Tests for the version endpoint.

    The version endpoint is critical for deployment verification.
    After deploying, the CI/CD pipeline hits this endpoint to confirm
    the correct version is running.
    """

    def test_version_returns_200(self, client):
        """Test that version endpoint returns HTTP 200 OK."""
        response = client.get('/version')
        assert response.status_code == 200

    def test_version_contains_version_number(self, client):
        """Test that version response includes version number."""
        response = client.get('/version')
        data = json.loads(response.data)
        assert 'version' in data
        assert data['version'] == '1.0.0'

    def test_version_contains_environment(self, client):
        """Test that version response includes environment."""
        response = client.get('/version')
        data = json.loads(response.data)
        assert 'environment' in data


# ============================================================================
# INFO ENDPOINT TESTS
# ============================================================================

class TestInfo:
    """Tests for the application info endpoint."""

    def test_info_returns_200(self, client):
        """Test that info endpoint returns HTTP 200 OK."""
        response = client.get('/info')
        assert response.status_code == 200

    def test_info_contains_hostname(self, client):
        """Test that info response includes hostname."""
        response = client.get('/info')
        data = json.loads(response.data)
        assert 'hostname' in data


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Tests for error handling."""

    def test_404_returns_json(self, client):
        """Test that 404 errors return JSON response."""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Not Found'


# ============================================================================
# ENVIRONMENT CONFIGURATION TESTS
# ============================================================================

class TestConfiguration:
    """Tests for environment-based configuration."""

    def test_default_environment(self, client):
        """Test that default environment is development."""
        response = client.get('/version')
        data = json.loads(response.data)
        assert data['environment'] == 'development'

    def test_custom_environment(self):
        """Test that environment can be set via env var."""
        import os
        os.environ['APP_ENV'] = 'production'
        app = create_app()
        assert app.config['APP_ENV'] == 'production'
        # Cleanup
        os.environ['APP_ENV'] = 'development'

