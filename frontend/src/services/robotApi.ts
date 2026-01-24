const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'; // Use environment variable or fallback to localhost
const USE_PROXY = import.meta.env.PROD; // Use proxy in production

class RobotAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = USE_PROXY ? '' : baseUrl; // Use relative URLs in production for proxy
  }

  async request(endpoint: string, options: RequestInit = {}) {
    try {
      const url = USE_PROXY ? `/api${endpoint}` : `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
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
    return this.request('/robot/start', {
      method: 'POST',
      body: JSON.stringify({ random_order: randomOrder, min_delay: minDelay, max_delay: maxDelay }),
    });
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

  // Speed Control
  async setSpeed(speed: number, acceleration: number) {
    return this.request('/robot/speed', {
      method: 'POST',
      body: JSON.stringify({ speed, acceleration }),
    });
  }

  async getSpeed() {
    return this.request('/robot/speed');
  }
}

export const robotApi = new RobotAPI();