from typing import Any, Dict, List

from app.position_manager import position_manager
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/training", tags=["training"])


class Position(BaseModel):
    id: str
    x: float
    y: float
    name: str
    description: str = ""


@router.get("/positions")
async def get_positions() -> List[Position]:
    return position_manager.get_positions()


@router.post("/positions")
async def save_positions(new_positions: List[Position]) -> Dict[str, Any]:
    try:
        position_manager.clear_positions()
        for position in new_positions:
            position_manager.add_position(position)
        return {"status": "success", "message": f"Saved {len(new_positions)} positions"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/positions/add")
async def add_position(position: Position) -> Dict[str, Any]:
    try:
        position_manager.add_position(position)
        return {"status": "success", "message": "Position added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/positions/{position_id}")
async def delete_position(position_id: str) -> Dict[str, Any]:
    try:
        position_manager.remove_position(position_id)
        return {"status": "success", "message": "Position deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sequence/start")
async def start_sequence(
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
        return {"status": "success", "message": "Sequence started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sequence/stop")
async def stop_sequence() -> Dict[str, Any]:
    try:
        position_manager.stop_sequence()
        return {"status": "success", "message": "Sequence stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sequence/status")
async def get_sequence_status() -> Dict[str, Any]:
    return {
        "is_running": position_manager.is_sequence_running(),
        "position_count": len(position_manager.get_positions()),
    }
