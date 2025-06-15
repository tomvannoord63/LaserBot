import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from robot.control import LaserRobot

load_dotenv()

robot = LaserRobot(
    ip=os.getenv("ROBOT_IP_ADDRESS"),
)
