import os

from dotenv import load_dotenv

from robot.control import LaserRobot

load_dotenv()

robot = LaserRobot(
    ip=os.getenv("ROBOT_IP_ADDRESS"),
)
