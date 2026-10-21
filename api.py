from fastapi import FastAPI,Depends
from robot import Robot
from pydantic import BaseModel
from typing import Literal


app = FastAPI()
robot = Robot("Robo")

def get_robot():    
    return robot


class RobotCommand(BaseModel):
    command: Literal["wake", "sleep"]

class RobotResponse(BaseModel):
    message: str
    status: Literal["awake", "sleeping"]


@app.get("/robot/status")
def get_robot_status(current_robot: Robot = Depends(get_robot)):
    return {
        "name": current_robot.name,
        "status": current_robot.status,
    }

@app.post("/robot/wake")
def wake_robot(current_robot: Robot = Depends(get_robot)):
    return {
        "message": current_robot.wake(),
        "status": current_robot.status,
    }

@app.post("/robot/sleep")
def sleep_robot(current_robot: Robot = Depends(get_robot)):
    return {
        "message": current_robot.sleep(),
        "status": current_robot.status,
    }

@app.post("/robot/command",response_model=RobotResponse)
def robot_command(request: RobotCommand, current_robot: Robot = Depends(get_robot)):
    if request.command == "wake":
        message = current_robot.wake()
    else:
        message = current_robot.sleep()

    return {
        "message": message,
        "status": current_robot.status,
    }