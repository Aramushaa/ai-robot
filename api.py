from fastapi import FastAPI,Depends
from robot import Robot
from pydantic import BaseModel
from typing import Literal
from database import save_command,get_command_history


app = FastAPI()
robot = Robot("Robo")

def get_robot():    
    return robot

def get_db_path():
    return "robot.db"


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
def robot_command(request: RobotCommand, current_robot: Robot = Depends(get_robot),
                  db_path:str = Depends(get_db_path)):
    status_before = current_robot.status
    if request.command == "wake":
        message = current_robot.wake()
    else:
        message = current_robot.sleep()
    status_after = current_robot.status

    save_command(request.command, status_before, status_after, 200, db_path=db_path)

    return {
        "message": message,
        "status": current_robot.status,
    }

@app.get("/robot/history")
def robot_history(db_path:str = Depends(get_db_path)):
    rows = get_command_history(db_path=db_path)

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "command": row[1],
            "status_before": row[2],
            "status_after": row[3],
            "http_status_code": row[4],
            "created_at": row[5]
        })

    return history