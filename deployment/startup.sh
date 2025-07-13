#!/bin/bash

# LaserBot Startup Script
# This script starts the backend service and frontend container for production

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Starting LaserBot services..."

# Start backend service (systemd will handle this, but ensure it's enabled)
echo "Ensuring backend service is enabled..."
sudo systemctl enable laserbot-backend.service
sudo systemctl start laserbot-backend.service

# Start frontend container
echo "Starting frontend container..."
cd "$PROJECT_DIR"
docker-compose -f deployment/docker-compose.prod.yml up -d

echo "LaserBot services started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"