from fastapi.testclient import TestClient
import api
import pytest
from robot import Robot
from database import init_db
import sqlite3



@pytest.fixture
def isolated_client(tmp_path):
    test_robot = Robot("Robo")
    db_path = tmp_path / "test_robot.db"
    init_db(db_path=db_path)

    def override_get_robot():
        return test_robot

    def override_get_db_path():
        return str(db_path)

    api.app.dependency_overrides[api.get_robot] = override_get_robot
    api.app.dependency_overrides[api.get_db_path] = override_get_db_path

    try:
        yield TestClient(api.app), db_path
    finally:
        api.app.dependency_overrides.clear()

        

def test_robot_status_endpoint(isolated_client):
    client, _ = isolated_client
    response = client.get("/robot/status")

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Robo"
    assert data["status"] == "sleeping"

def test_invalid_command(isolated_client):
    client, _ = isolated_client
    before = client.get("/robot/status")
    assert before.status_code == 200

    initial_status = before.json()["status"]

    response = client.post(
        "/robot/command",
        json={"command": "dance"}
    )
    assert response.status_code == 422

    after = client.get("/robot/status")
    assert after.status_code == 200

    final_status = after.json()["status"]

    assert final_status == initial_status


def test_command_uses_isolated_robot(isolated_client):
    client, _ = isolated_client
    original_status = api.robot.status


    response = client.post(
        "/robot/command",
        json={"command": "wake"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "awake"


    status_response = client.get("/robot/status")

    assert status_response.status_code == 200
    assert status_response.json()["status"] == "awake"


    assert api.robot.status == original_status


def test_command_saved_to_database(isolated_client):
    client, db_path = isolated_client
    response = client.post(
        "/robot/command",
        json={"command": "wake"}
    )

    connection = sqlite3.connect(db_path)
    row = connection.execute("""SELECT command, status_before, status_after, http_status_code
        FROM robot_commands
        ORDER BY id DESC
        LIMIT 1;""").fetchone()

    connection.close()
    assert response.status_code == 200
    assert row == ("wake", "sleeping", "awake", 200)

def test_repeated_wake_is_logged(isolated_client):
    client, db_path = isolated_client
    response1 = client.post(
        "/robot/command",
        json={"command": "wake"}
    )
    response2 = client.post(
        "/robot/command",
        json={"command": "wake"}
    )

    connection = sqlite3.connect(db_path)
    rows = connection.execute("""SELECT command, status_before, status_after
        FROM robot_commands
        ORDER BY id ASC;""").fetchall()

    connection.close()

    assert rows == [
        ("wake", "sleeping", "awake"),
        ("wake", "awake", "awake"),
    ]
    assert response1.status_code == 200
    assert response2.status_code == 200
    

def test_robot_history_endpoint(isolated_client):
    client, _ = isolated_client

    client.post("/robot/command", json={"command": "wake"})
    client.post("/robot/command", json={"command": "sleep"})

    response = client.get("/robot/history")

    assert response.status_code == 200

    history = response.json()

    assert len(history) == 2
    assert history[0]["command"] == "sleep"
    assert history[1]["command"] == "wake"