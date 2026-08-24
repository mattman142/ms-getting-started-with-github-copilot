from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_adds_participant():
    # Arrange
    activity_name = "Basketball Team"
    email = f"{uuid4()}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Basketball Team"
    email = f"{uuid4()}@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    # Arrange
    activity_name = "Basketball Team"
    email = f"{uuid4()}@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"{email} removed from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unknown_activity_returns_404():
    # Arrange
    activity_name = "Not Real Activity"
    email = f"{uuid4()}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
