import socket
import struct
import time
import threading
from threading import Event, Thread
from typing import Optional, Tuple, Dict, Any
import logging


logger = logging.getLogger(__name__)


class LaserRobot:
    """A class to control the laser pointer robot."""

    def __init__(
        self, ip: str = "YOUR.IP.ADDRESS.HERE", port: int = 2222, in_port: int = 2223
    ):
        """Initialize the laser robot with connection parameters.

        Args:
            ip: The IP address of the robot
            port: The port for sending commands
            in_port: The port for receiving telemetry
        """
        self.ip = ip
        self.port = port
        self.in_port = in_port
        self.socket: Optional[socket.socket] = None
        self.telemetry_socket: Optional[socket.socket] = None
        self.exit_event = Event()
        self.current_angles: Tuple[float, float] = (0.0, 0.0)
        self.laser_on: bool = True  # Track laser state
        self.telemetry_thread: Optional[Thread] = None
        self.telemetry_running = False
        self.latest_telemetry: Dict[str, Any] = {
            "angle1": 0.0,
            "angle2": 0.0,
            "speed1": 0,
            "speed2": 0,
            "last_update": None
        }

    def connect(self) -> bool:
        """Establish connection with the robot.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create command socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.sendto(b"JJAH0000000000000000", (self.ip, self.port))
            # Set initial speed and acceleration
            self.send_command(b"JJAS", 50, 0, 70, 0)  # 50% speed, 70% accel

            # Start telemetry listener
            self.start_telemetry_listener()

            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def disconnect(self) -> None:
        """Close the connection to the robot."""
        # Stop telemetry listener
        self.stop_telemetry_listener()

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
        self.laser_on = True

    def turn_laser_off(self) -> None:
        """Turn the laser off."""
        self.send_command(b"JJOF")
        self.laser_on = False

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

    def start_telemetry_listener(self) -> None:
        """Start listening for telemetry data from the robot."""
        if self.telemetry_running:
            return

        try:
            # Create UDP socket for receiving telemetry
            self.telemetry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.telemetry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.telemetry_socket.bind(("0.0.0.0", self.in_port))
            self.telemetry_socket.settimeout(1.0)  # 1 second timeout for checking stop flag

            self.telemetry_running = True
            self.telemetry_thread = Thread(target=self._telemetry_listener_loop, daemon=True)
            self.telemetry_thread.start()
            logger.info(f"Telemetry listener started on port {self.in_port}")
        except Exception as e:
            logger.error(f"Failed to start telemetry listener: {e}")

    def stop_telemetry_listener(self) -> None:
        """Stop the telemetry listener thread."""
        if not self.telemetry_running:
            return

        self.telemetry_running = False
        if self.telemetry_thread:
            self.telemetry_thread.join(timeout=2.0)
            self.telemetry_thread = None

        if self.telemetry_socket:
            self.telemetry_socket.close()
            self.telemetry_socket = None

        logger.info("Telemetry listener stopped")

    def _telemetry_listener_loop(self) -> None:
        """Background thread that listens for telemetry data."""
        logger.info("Telemetry listener loop started")
        while self.telemetry_running:
            try:
                data, addr = self.telemetry_socket.recvfrom(1024)
                self._parse_telemetry(data.decode('utf-8', errors='ignore'))
            except socket.timeout:
                # Normal timeout, continue loop
                continue
            except Exception as e:
                if self.telemetry_running:  # Only log if we're still supposed to be running
                    logger.error(f"Error receiving telemetry: {e}")

    def _parse_telemetry(self, data: str) -> None:
        """Parse telemetry data from the robot.

        Expected format: #<angle1>,<angle2>,<speed1>,<speed2>
        Example: #12.34,56.78,100,150
        """
        try:
            # Remove leading # and split by comma
            if not data.startswith('#'):
                return

            parts = data[1:].strip().split(',')
            if len(parts) >= 4:
                self.latest_telemetry = {
                    "angle1": float(parts[0]),
                    "angle2": float(parts[1]),
                    "speed1": int(parts[2]),
                    "speed2": int(parts[3]),
                    "last_update": time.time()
                }
                # Update current_angles with telemetry data
                self.current_angles = (self.latest_telemetry["angle1"], self.latest_telemetry["angle2"])
                logger.debug(f"Telemetry: {self.latest_telemetry}")
        except Exception as e:
            logger.error(f"Failed to parse telemetry: {data}, error: {e}")

    def get_telemetry(self) -> Dict[str, Any]:
        """Get the latest telemetry data.

        Returns:
            Dictionary containing angle1, angle2, speed1, speed2, and last_update timestamp
        """
        return self.latest_telemetry.copy()
