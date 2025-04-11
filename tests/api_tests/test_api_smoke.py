from fastapi.testclient import TestClient

from src.kronoterm_cloud_relay import app

client = TestClient(app)


def test_about():
    """
    FEATURE: ROOT ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain 'detail' as 'kronoterm-cloud-relay' and 'version' as '0.0.22'
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "kronoterm-cloud-relay", "version": "0.0.22"}


def test_info_summary():
    """
    FEATURE: INFO SUMMARY ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/info-summary' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/info-summary")
    assert response.status_code == 200
    assert "data" in response.json()


def test_initial_data():
    """FEATURE: INITIAL DATA ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/initial-data' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/initial-data")
    assert response.status_code == 200
    assert "data" in response.json()


def test_basic_data():
    """FEATURE: BASIC DATA ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/basic-data' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/basic-data")
    assert response.status_code == 200
    assert "data" in response.json()


def test_system_review():
    """FEATURE: SYSTEM REVIEW ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/system-review' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/system-review")
    assert response.status_code == 200
    assert "data" in response.json()


def test_alarms():
    """FEATURE: ALARMS ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/alarms' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/alarms")
    assert response.status_code == 200
    assert "data" in response.json()


def test_echo():
    """FEATURE: ECHO ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'POST' request is sent to the '/api/v1/echo/{msg}' endpoint with a message
    THEN the response status code should be '200'
    AND the response JSON should echo the same message
    """
    msg = "test-message"
    response = client.post(f"/api/v1/echo/{msg}")
    assert response.status_code == 200
    assert response.json() == {"echo": msg}
