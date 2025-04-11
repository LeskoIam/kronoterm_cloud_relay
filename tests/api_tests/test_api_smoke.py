import logging

from fastapi.testclient import TestClient

from src.kronoterm_cloud_relay import app

client = TestClient(app)

log = logging.getLogger("pytest")


def test_about():
    """
    FEATURE: ROOT ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain 'detail' as 'kronoterm-cloud-relay' and 'version' as '0.0.22'

    ## Note: The version number used for test is automatically updated in the code at build time.
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

    data_keys = [
        "hp_id",
        "location_name",
        "user_level",
        "heating_loop_names",
        "alarms",
        "heat_pump_operating_mode",
        "system_info",
        "heating_loop_1",
        "heating_loop_2",
        "heating_loop_5",
    ]

    response = client.get("/api/v1/info-summary")
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    for data_key in data_keys:
        log.info("Mandatory key '%s' is present in response", data_key)
        assert data_key in response_json["data"]


def test_initial_data():
    """
    FEATURE: INITIAL DATA ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/initial-data' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/initial-data")
    assert response.status_code == 200
    assert "data" in response.json()


def test_basic_data():
    """
    FEATURE: BASIC DATA ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/basic-data' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/basic-data")
    assert response.status_code == 200
    assert "data" in response.json()


def test_system_review():
    """
    FEATURE: SYSTEM REVIEW ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/system-review' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/system-review")
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert response_json["data"]["tableName"] == "System review"


def test_alarms():
    """
    FEATURE: ALARMS ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'GET' request is sent to the '/api/v1/alarms' endpoint
    THEN the response status code should be '200'
    AND the response JSON should contain a 'data' field
    """
    response = client.get("/api/v1/alarms")
    assert response.status_code == 200
    assert "data" in response.json()


def test_echo():
    """
    FEATURE: ECHO ENDPOINT
    GIVEN the FastAPI application is running
    WHEN the 'POST' request is sent to the '/api/v1/echo/{msg}' endpoint with a message
    THEN the response status code should be '200'
    AND the response JSON should echo the same message
    """
    msg = "test-message"
    response = client.post(f"/api/v1/echo/{msg}")
    assert response.status_code == 200
    assert response.json() == {"echo": msg}
