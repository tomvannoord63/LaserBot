import random
import time
from threading import Event
from typing import List, Optional

from app.robot import robot
from app.routes.training_routes import Position


class PositionManager:
    def __init__(self):
        self.positions: List[Position] = []
        self.exit_event = Event()
        self.is_running = False

    def add_position(self, position: Position) -> None:
        """Add a new position to the list."""
        self.positions.append(position)

    def remove_position(self, position_id: str) -> None:
        """Remove a position by its ID."""
        self.positions = [p for p in self.positions if p.id != position_id]

    def clear_positions(self) -> None:
        """Clear all positions."""
        self.positions.clear()

    def get_positions(self) -> List[Position]:
        """Get all positions."""
        return self.positions

    def move_to_position(self, position: Position, delay: float = 0.5) -> None:
        """Move the robot to a specific position."""
        robot.move_to_angles_with_delay(position.x, position.y, delay)

    def start_sequence(
        self, random_order: bool = True, min_delay: float = 3.0, max_delay: float = 5.0
    ) -> None:
        """Start a sequence of movements through all positions."""
        if not self.positions:
            return

        self.is_running = True
        self.exit_event.clear()

        try:
            while not self.exit_event.is_set():
                # Create a sequence of position indices
                sequence = list(range(len(self.positions)))
                if random_order:
                    random.shuffle(sequence)

                # Move through each position
                for idx in sequence:
                    if self.exit_event.is_set():
                        break

                    position = self.positions[idx]
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
