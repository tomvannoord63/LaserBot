from typing import Any, Dict, List, Optional

from app.position_manager import position_manager
from app.robot import robot
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel


class LaserToggleRequest(BaseModel):
    on: bool


class LaserMoveRequest(BaseModel):
    x: float
    y: float


class RobotStartRequest(BaseModel):
    random_order: bool = True
    min_delay: float = 3.0
    max_delay: float = 5.0


class LaserPosition(BaseModel):
    id: str
    x: float
    y: float
    name: str
    duration: Optional[float] = None


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
async def start_robot(request: RobotStartRequest) -> Dict[str, Any]:
    try:
        if position_manager.is_sequence_running():
            raise HTTPException(status_code=400, detail="A sequence is already running")

        # Start the sequence in a background task
        import asyncio

        asyncio.create_task(
            asyncio.to_thread(
                position_manager.start_sequence,
                random_order=request.random_order,
                min_delay=request.min_delay,
                max_delay=request.max_delay,
            )
        )
        return {"status": "running", "message": "Robot started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_robot() -> Dict[str, Any]:
    try:
        position_manager.stop_sequence()
        return {"status": "stopped", "message": "Robot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_robot_status() -> Dict[str, Any]:
    try:
        print(robot.laser_on)
        return {
            "status": "running" if position_manager.is_sequence_running() else "idle",
            "connected": robot.socket is not None,
            "laser_on": robot.laser_on,
            "position": {"x": robot.current_angles[0], "y": robot.current_angles[1]},
            "sequence": {
                "is_running": position_manager.is_sequence_running(),
                "position_count": len(position_manager.get_positions()),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Laser Control
@router.post("/laser/toggle")
async def toggle_laser(request: LaserToggleRequest) -> Dict[str, Any]:
    try:
        if request.on:
            robot.turn_laser_on()
        else:
            robot.turn_laser_off()
        return {"status": "success", "laser_on": request.on}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/laser/move")
async def move_laser(request: LaserMoveRequest) -> Dict[str, Any]:
    try:
        robot.move_to_angles(request.x, request.y)
        return {"status": "success", "position": {"x": request.x, "y": request.y}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Training/Configuration
@router.get("/training/positions")
async def get_positions() -> Dict[str, List[LaserPosition]]:
    try:
        positions = position_manager.get_positions()
        return {"positions": positions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/training/positions")
async def save_positions(positions: List[LaserPosition]) -> Dict[str, Any]:
    try:
        position_manager.save_positions(positions)
        return {"status": "success", "message": "Positions saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/training/positions/add")
async def add_position(position: LaserPosition) -> Dict[str, Any]:
    try:
        position_manager.add_position(position)
        return {"status": "success", "message": "Position added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/training/positions/{id}")
async def delete_position(id: str) -> Dict[str, Any]:
    try:
        position_manager.delete_position(id)
        return {"status": "success", "message": "Position deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
