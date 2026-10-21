from fastapi.testclient import TestClient
import api
import pytest
from robot import Robot



@pytest.fixture
def isolated_client():
    test_robot = Robot("Robo")

    def override_get_robot():
        return test_robot

    api.app.dependency_overrides[api.get_robot] = override_get_robot

    try:
        yield TestClient(api.app)
    finally:
        api.app.dependency_overrides.clear()

        

def test_robot_status_endpoint(isolated_client):
    response = isolated_client.get("/robot/status")

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Robo"
    assert data["status"] == "sleeping"

def test_invalid_command(isolated_client):
    before = isolated_client.get("/robot/status")
    assert before.status_code == 200

    initial_status = before.json()["status"]

    response = isolated_client.post(
        "/robot/command",
        json={"command": "dance"}
    )
    assert response.status_code == 422

    after = isolated_client.get("/robot/status")
    assert after.status_code == 200

    final_status = after.json()["status"]

    assert final_status == initial_status


def test_command_uses_isolated_robot(isolated_client):
    original_status = api.robot.status


    response = isolated_client.post(
        "/robot/command",
        json={"command": "wake"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "awake"


    status_response = isolated_client.get("/robot/status")

    assert status_response.status_code == 200
    assert status_response.json()["status"] == "awake"


    assert api.robot.status == original_status