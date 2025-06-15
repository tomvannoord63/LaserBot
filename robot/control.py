import socket
import struct
import time
from threading import Event
from typing import Optional, Tuple


class LaserRobot:
    """A class to control the laser pointer robot."""

    def __init__(
        self, ip: str = "YOUR.IP.ADDRESS.HERE", port: int = 2222, in_port: int = 2223
    ):
        """Initialize the laser robot with connection parameters.

        Args:
            ip: The IP address of the robot
            port: The port for sending commands
            in_port: The port for receiving input
        """
        self.ip = ip
        self.port = port
        self.in_port = in_port
        self.socket: Optional[socket.socket] = None
        self.exit_event = Event()
        self.current_angles: Tuple[float, float] = (0.0, 0.0)

    def connect(self) -> bool:
        """Establish connection with the robot.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.sendto(b"JJAH0000000000000000", (self.ip, self.port))
            # Set initial speed and acceleration
            self.send_command(b"JJAS", 50, 0, 70, 0)  # 50% speed, 70% accel
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self) -> None:
        """Close the connection to the robot."""
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_command(
        self,
        header: bytes,
        p1: int = 0,
        p2: int = 0,
        p3: int = 0,
        p4: int = 0,
        p5: int = 0,
        p6: int = 0,
        p7: int = 0,
        p8: int = 0,
    ) -> None:
        """Send a command to the robot.

        Args:
            header: Command header (e.g., b'JJAM' for move, b'JJON' for laser on)
            p1-p8: Command parameters
        """
        if not self.socket:
            raise ConnectionError("Not connected to robot")

        message = bytearray(header)
        for param in [p1, p2, p3, p4, p5, p6, p7, p8]:
            message.extend(bytearray(struct.pack(">h", param)))

        try:
            self.socket.sendto(message, (self.ip, self.port))
        except Exception as e:
            print(f"Failed to send command: {e}")

    def move_to_angles(self, angle1: float, angle2: float) -> None:
        """Move the robot to specified angles.

        Args:
            angle1: First axis angle in degrees
            angle2: Second axis angle in degrees
        """
        self.current_angles = (angle1, angle2)
        self.send_command(b"JJAM", int(angle1 * 100), int(angle2 * 100))

    def move_to_angles_with_delay(
        self, angle1: float, angle2: float, delay: float = 0.5
    ) -> None:
        """Move the robot to specified angles and wait for specified delay.

        Args:
            angle1: First axis angle in degrees
            angle2: Second axis angle in degrees
            delay: Time to wait after movement in seconds
        """
        self.move_to_angles(angle1, angle2)
        time.sleep(delay)

    def turn_laser_on(self) -> None:
        """Turn the laser on."""
        self.send_command(b"JJON")

    def turn_laser_off(self) -> None:
        """Turn the laser off."""
        self.send_command(b"JJOF")

    def set_speed_and_acceleration(self, speed: int, acceleration: int) -> None:
        """Set the robot's speed and acceleration.

        Args:
            speed: Speed percentage (0-100)
            acceleration: Acceleration percentage (0-100)
        """
        self.send_command(b"JJAS", speed, 0, acceleration, 0)

    def stop(self) -> None:
        """Stop the robot and return to home position."""
        self.exit_event.set()
        time.sleep(2)  # Wait for any ongoing movements to complete
        self.move_to_angles(0, 0)
        self.exit_event.clear()
