from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/training", tags=["training"])


class Position(BaseModel):
    id: str
    x: float
    y: float
    name: str
    description: str = ""


# In-memory storage for positions (replace with database in production)
positions: List[Position] = []


@router.get("/positions")
async def get_positions() -> List[Position]:
    return positions


@router.post("/positions")
async def save_positions(new_positions: List[Position]) -> Dict[str, Any]:
    try:
        positions.clear()
        positions.extend(new_positions)
        return {"status": "success", "message": f"Saved {len(new_positions)} positions"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/positions/add")
async def add_position(position: Position) -> Dict[str, Any]:
    try:
        positions.append(position)
        return {"status": "success", "message": "Position added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/positions/{position_id}")
async def delete_position(position_id: str) -> Dict[str, Any]:
    try:
        global positions
        positions = [p for p in positions if p.id != position_id]
        return {"status": "success", "message": "Position deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
