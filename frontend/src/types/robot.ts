export interface RobotStatus {
  connected: boolean;
  running: boolean;
  laserOn: boolean;
  battery?: number;
  lastHeartbeat?: Date;
}

export interface LaserPosition {
  id: string;
  x: number;
  y: number;
  name: string;
  duration?: number;
}

export interface RobotConfig {
  positions: LaserPosition[];
  speed: number;
  autoMode: boolean;
}