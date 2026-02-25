from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert pattern for FastAPI endpoints

def test_get_activities():
    # Arrange: nothing to setup, use default app state
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert len(response.json()) >= 0

def test_signup_success():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    # Confirm participant added
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants

def test_signup_duplicate():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code != 200 or "detail" in response.json()


def test_unregister_success():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    # Confirm participant removed
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_unregister_not_found():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "notfound@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404 or "detail" in response.json()
