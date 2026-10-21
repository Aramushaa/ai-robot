from robot import Robot
from pytest import fixture

@fixture
def fresh_robot():
    return Robot("Robo")

def test_robot_wakes_up(fresh_robot):
    message = fresh_robot.wake()

    assert fresh_robot.status == "awake"
    assert message == "Robo is now awake!"

def test_wake_is_idempotent(fresh_robot):
    robot = fresh_robot
    assert robot.status == "sleeping"
    message = robot.wake()
    assert robot.status == "awake"
    assert message == "Robo is now awake!"
    message = robot.wake()
    assert robot.status == "awake"
    assert message == "Robo is already awake!"