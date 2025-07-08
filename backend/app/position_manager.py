import logging
import random
import time
from threading import Event
from typing import List

from app.database import SessionLocal
from app.models.position_model import PositionModel
from app.robot import robot
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        try:
            logger.debug("Creating database session")
            return SessionLocal()
        except Exception as e:
            logger.error(f"Error creating database session: {str(e)}")
            raise

    def add_position(self, position: Position) -> None:
        """Add a new position to the database."""
        logger.info(f"Adding position: id={position.id}, name={position.name}, x={position.x}, y={position.y}")
        db = self._get_db()
        try:
            # Check if position already exists
            existing_position = db.query(PositionModel).filter(PositionModel.id == position.id).first()
            if existing_position:
                logger.warning(f"Position with id={position.id} already exists, will not add duplicate")
                raise ValueError(f"Position with id {position.id} already exists")
            
            db_position = PositionModel(
                id=position.id,
                x=position.x,
                y=position.y,
                name=position.name,
                description=position.description,
            )
            logger.debug(f"Created PositionModel object: {db_position}")
            db.add(db_position)
            db.commit()
            logger.info(f"Successfully added position: id={position.id}")
        except Exception as e:
            logger.error(f"Error adding position id={position.id}: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def remove_position(self, position_id: str) -> None:
        """Remove a position by its ID from the database."""
        logger.info(f"Removing position: id={position_id}")
        db = self._get_db()
        try:
            position = (
                db.query(PositionModel).filter(PositionModel.id == position_id).first()
            )
            if position:
                logger.debug(f"Found position to remove: {position.name}")
                db.delete(position)
                db.commit()
                logger.info(f"Successfully removed position: id={position_id}")
            else:
                logger.warning(f"Position with id={position_id} not found for removal")
        except Exception as e:
            logger.error(f"Error removing position id={position_id}: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def clear_positions(self) -> None:
        """Clear all positions from the database."""
        logger.info("Clearing all positions from database")
        db = self._get_db()
        try:
            deleted_count = db.query(PositionModel).delete()
            db.commit()
            logger.info(f"Successfully cleared {deleted_count} positions from database")
        except Exception as e:
            logger.error(f"Error clearing positions: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def get_positions(self) -> List[Position]:
        """Get all positions from the database."""
        logger.debug("Fetching all positions from database")
        db = self._get_db()
        try:
            db_positions = db.query(PositionModel).all()
            positions = [
                Position(
                    id=pos.id,
                    x=pos.x,
                    y=pos.y,
                    name=pos.name,
                    description=pos.description,
                )
                for pos in db_positions
            ]
            logger.debug(f"Found {len(positions)} positions in database")
            return positions
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            raise
        finally:
            db.close()

    def get_position_by_id(self, position_id: str) -> Position | None:
        """Get a specific position by ID."""
        logger.debug(f"Fetching position by id: {position_id}")
        db = self._get_db()
        try:
            db_position = (
                db.query(PositionModel).filter(PositionModel.id == position_id).first()
            )
            if db_position:
                logger.debug(f"Found position: {db_position.name}")
                return Position(
                    id=db_position.id,
                    x=db_position.x,
                    y=db_position.y,
                    name=db_position.name,
                    description=db_position.description,
                )
            logger.debug(f"Position with id={position_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching position by id={position_id}: {str(e)}")
            raise
        finally:
            db.close()

    def update_position(self, position: Position) -> None:
        """Update an existing position in the database."""
        logger.info(f"Updating position: id={position.id}, name={position.name}")
        db = self._get_db()
        try:
            db_position = (
                db.query(PositionModel).filter(PositionModel.id == position.id).first()
            )
            if db_position:
                logger.debug(f"Found position to update: {db_position.name}")
                db_position.x = position.x
                db_position.y = position.y
                db_position.name = position.name
                db_position.description = position.description
                db.commit()
                logger.info(f"Successfully updated position: id={position.id}")
            else:
                logger.warning(f"Position with id={position.id} not found for update")
                raise ValueError(f"Position with id {position.id} not found")
        except Exception as e:
            logger.error(f"Error updating position id={position.id}: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def move_to_position(self, position: Position, delay: float = 0.5) -> None:
        """Move the robot to a specific position."""
        logger.info(f"Moving robot to position: {position.name} (x={position.x}, y={position.y})")
        try:
            robot.move_to_angles_with_delay(position.x, position.y, delay)
            logger.info(f"Successfully moved to position: {position.name}")
        except Exception as e:
            logger.error(f"Error moving to position {position.name}: {str(e)}")
            raise

    def start_sequence(
        self, random_order: bool = True, min_delay: float = 3.0, max_delay: float = 5.0
    ) -> None:
        """Start a sequence of movements through all positions."""
        logger.info(f"Starting position sequence: random_order={random_order}, delays={min_delay}-{max_delay}s")
        positions = self.get_positions()
        if not positions:
            logger.warning("No positions available for sequence")
            return

        logger.info(f"Starting sequence with {len(positions)} positions")
        self.is_running = True
        self.exit_event.clear()

        try:
            while not self.exit_event.is_set():
                # Create a sequence of position indices
                sequence = list(range(len(positions)))
                if random_order:
                    random.shuffle(sequence)
                    logger.debug(f"Randomized sequence order: {sequence}")

                # Move through each position
                for idx in sequence:
                    if self.exit_event.is_set():
                        logger.info("Sequence interrupted by exit event")
                        break

                    position = positions[idx]
                    delay = random.uniform(min_delay, max_delay)
                    logger.debug(f"Moving to position {idx+1}/{len(positions)}: {position.name} (delay={delay:.2f}s)")
                    self.move_to_position(position, delay)

                # Optional: Add a pause between sequences
                if not self.exit_event.is_set():
                    logger.debug("Returning to home position")
                    robot.move_to_angles(0, 0)  # Return to home position
                    time.sleep(2)  # Pause between sequences

        except Exception as e:
            logger.error(f"Error during sequence execution: {str(e)}")
            raise
        finally:
            self.is_running = False
            logger.info("Position sequence stopped")

    def stop_sequence(self) -> None:
        """Stop the current sequence."""
        logger.info("Stopping position sequence")
        self.exit_event.set()
        try:
            robot.stop()
            logger.info("Successfully stopped robot and sequence")
        except Exception as e:
            logger.error(f"Error stopping robot: {str(e)}")
            raise

    def is_sequence_running(self) -> bool:
        """Check if a sequence is currently running."""
        return self.is_running


# Create a singleton instance
position_manager = PositionManager()
