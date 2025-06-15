const API_BASE_URL = 'http://localhost:8000'; // Update this to match your FastAPI server

class RobotAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Robot Control
  async connectRobot() {
    return this.request('/robot/connect', { method: 'POST' });
  }

  async disconnectRobot() {
    return this.request('/robot/disconnect', { method: 'POST' });
  }

  async startRobot(randomOrder: boolean = true, minDelay: number = 3.0, maxDelay: number = 5.0) {
    return this.request(`/robot/start?random_order=${randomOrder}&min_delay=${minDelay}&max_delay=${maxDelay}`, { method: 'POST' });
  }

  async stopRobot() {
    return this.request('/robot/stop', { method: 'POST' });
  }

  async getRobotStatus() {
    return this.request('/robot/status');
  }

  // Laser Control
  async toggleLaser(on: boolean) {
    return this.request('/robot/laser/toggle', {
      method: 'POST',
      body: JSON.stringify({ on }),
    });
  }

  async moveLaser(x: number, y: number) {
    return this.request('/robot/laser/move', {
      method: 'POST',
      body: JSON.stringify({ x, y }),
    });
  }

  // Training/Configuration
  async getPositions() {
    return this.request('/training/positions');
  }

  async savePositions(positions: any[]) {
    return this.request('/training/positions', {
      method: 'POST',
      body: JSON.stringify(positions),
    });
  }

  async addPosition(position: any) {
    return this.request('/training/positions/add', {
      method: 'POST',
      body: JSON.stringify(position),
    });
  }

  async deletePosition(id: string) {
    return this.request(`/training/positions/${id}`, {
      method: 'DELETE',
    });
  }
}

export const robotApi = new RobotAPI();