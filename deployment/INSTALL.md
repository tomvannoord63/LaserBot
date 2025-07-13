# LaserBot Raspberry Pi Installation Guide

## Prerequisites
- Raspberry Pi with Raspberry Pi OS
- Docker and Docker Compose installed
- uv installed for Python dependency management
- User account: `bot` (as configured in systemd service)

## Installation Steps

### 1. Clone Repository
```bash
cd /home/bot
git clone <repository-url> LaserBot
cd LaserBot
```

### 2. Install Backend Dependencies
```bash
cd backend
uv sync
```

### 3. Create Environment File
```bash
cp .env.example .env
# Edit .env to set ROBOT_IP_ADDRESS
```

### 4. Install Systemd Service
```bash
sudo cp deployment/laserbot-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable laserbot-backend.service
```

### 5. Start Services
```bash
# Option 1: Use startup script
./deployment/startup.sh

# Option 2: Manual start
sudo systemctl start laserbot-backend.service
docker-compose -f deployment/docker-compose.prod.yml up -d
```

## Access
- Frontend: http://raspberrypi.local:3000 or http://<pi-ip>:3000
- Backend API: http://raspberrypi.local:8000 or http://<pi-ip>:8000

## Service Management
```bash
# Check backend status
sudo systemctl status laserbot-backend.service

# Check frontend container
docker-compose -f deployment/docker-compose.prod.yml ps

# View logs
sudo journalctl -u laserbot-backend.service -f
docker-compose -f deployment/docker-compose.prod.yml logs -f
```

## Auto-start on Boot
Services are configured to start automatically:
- Backend: systemd service with `WantedBy=multi-user.target`
- Frontend: Docker container with `restart: unless-stopped`