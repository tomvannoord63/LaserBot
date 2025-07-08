import random
import time
from threading import Event
from typing import List

from app.database import SessionLocal
from app.models.position_model import PositionModel
from app.robot import robot
from pydantic import BaseModel


class Position(BaseModel):
    id: str
    x: float
    y: float
    name: str
    description: str = ""


class PositionManager:
    def __init__(self):
        self.exit_event = Event()
        self.is_running = False

    def _get_db(self):
        """Get a database session."""
        return SessionLocal()

    def add_position(self, position: Position) -> None:
        """Add a new position to the database."""
        db = self._get_db()
        try:
            db_position = PositionModel(
                id=position.id,
                x=position.x,
                y=position.y,
                name=position.name,
                description=position.description,
            )
            db.add(db_position)
            db.commit()
        finally:
            db.close()

    def remove_position(self, position_id: str) -> None:
        """Remove a position by its ID from the database."""
        db = self._get_db()
        try:
            position = (
                db.query(PositionModel).filter(PositionModel.id == position_id).first()
            )
            if position:
                db.delete(position)
                db.commit()
        finally:
            db.close()

    def clear_positions(self) -> None:
        """Clear all positions from the database."""
        db = self._get_db()
        try:
            db.query(PositionModel).delete()
            db.commit()
        finally:
            db.close()

    def get_positions(self) -> List[Position]:
        """Get all positions from the database."""
        db = self._get_db()
        try:
            db_positions = db.query(PositionModel).all()
            return [
                Position(
                    id=pos.id,
                    x=pos.x,
                    y=pos.y,
                    name=pos.name,
                    description=pos.description,
                )
                for pos in db_positions
            ]
        finally:
            db.close()

    def get_position_by_id(self, position_id: str) -> Position | None:
        """Get a specific position by ID."""
        db = self._get_db()
        try:
            db_position = (
                db.query(PositionModel).filter(PositionModel.id == position_id).first()
            )
            if db_position:
                return Position(
                    id=db_position.id,
                    x=db_position.x,
                    y=db_position.y,
                    name=db_position.name,
                    description=db_position.description,
                )
            return None
        finally:
            db.close()

    def update_position(self, position: Position) -> None:
        """Update an existing position in the database."""
        db = self._get_db()
        try:
            db_position = (
                db.query(PositionModel).filter(PositionModel.id == position.id).first()
            )
            if db_position:
                db_position.x = position.x
                db_position.y = position.y
                db_position.name = position.name
                db_position.description = position.description
                db.commit()
        finally:
            db.close()

    def move_to_position(self, position: Position, delay: float = 0.5) -> None:
        """Move the robot to a specific position."""
        robot.move_to_angles_with_delay(position.x, position.y, delay)

    def start_sequence(
        self, random_order: bool = True, min_delay: float = 3.0, max_delay: float = 5.0
    ) -> None:
        """Start a sequence of movements through all positions."""
        positions = self.get_positions()
        if not positions:
            return

        self.is_running = True
        self.exit_event.clear()

        try:
            while not self.exit_event.is_set():
                # Create a sequence of position indices
                sequence = list(range(len(positions)))
                if random_order:
                    random.shuffle(sequence)

                # Move through each position
                for idx in sequence:
                    if self.exit_event.is_set():
                        break

                    position = positions[idx]
                    delay = random.uniform(min_delay, max_delay)
                    self.move_to_position(position, delay)

                # Optional: Add a pause between sequences
                if not self.exit_event.is_set():
                    robot.move_to_angles(0, 0)  # Return to home position
                    time.sleep(2)  # Pause between sequences

        finally:
            self.is_running = False

    def stop_sequence(self) -> None:
        """Stop the current sequence."""
        self.exit_event.set()
        robot.stop()

    def is_sequence_running(self) -> bool:
        """Check if a sequence is currently running."""
        return self.is_running


# Create a singleton instance
position_manager = PositionManager()
