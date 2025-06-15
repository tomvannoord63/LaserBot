from typing import Any, Dict

from app.robot import robot
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/robot", tags=["robot"])


# Robot Control
@router.post("/connect")
async def connect_robot() -> Dict[str, Any]:
    try:
        if robot.connect():
            return {"status": "connected", "message": "Robot connected successfully"}
        raise HTTPException(status_code=500, detail="Failed to connect to robot")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disconnect")
async def disconnect_robot() -> Dict[str, Any]:
    try:
        robot.disconnect()
        return {"status": "disconnected", "message": "Robot disconnected successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_robot() -> Dict[str, Any]:
    try:
        # TODO: Implement actual robot start logic
        return {"status": "running", "message": "Robot started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_robot() -> Dict[str, Any]:
    try:
        robot.stop()
        return {"status": "stopped", "message": "Robot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_robot_status() -> Dict[str, Any]:
    try:
        return {
            "status": "idle",
            "connected": robot.socket is not None,
            "laser_on": False,  # You might want to add a state variable to track this
            "position": {"x": robot.current_angles[0], "y": robot.current_angles[1]},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Laser Control
@router.post("/laser/toggle")
async def toggle_laser(on: bool) -> Dict[str, Any]:
    try:
        if on:
            robot.turn_laser_on()
        else:
            robot.turn_laser_off()
        return {"status": "success", "laser_on": on}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/laser/move")
async def move_laser(x: float, y: float) -> Dict[str, Any]:
    try:
        robot.move_to_angles(x, y)
        return {"status": "success", "position": {"x": x, "y": y}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
