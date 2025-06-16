from typing import Any, Dict

from app.position_manager import position_manager
from app.robot import robot
from fastapi import APIRouter, HTTPException, Query

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
async def start_robot(
    random_order: bool = True, min_delay: float = 3.0, max_delay: float = 5.0
) -> Dict[str, Any]:
    try:
        if position_manager.is_sequence_running():
            raise HTTPException(status_code=400, detail="A sequence is already running")

        # Start the sequence in a background task
        import asyncio

        asyncio.create_task(
            asyncio.to_thread(
                position_manager.start_sequence,
                random_order=random_order,
                min_delay=min_delay,
                max_delay=max_delay,
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
async def toggle_laser(
    on: bool = Query(..., description="Whether to turn the laser on or off")
) -> Dict[str, Any]:
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
