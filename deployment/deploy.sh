#!/bin/bash

# LaserBot Deployment Script for ARMv6l Raspberry Pi
# Builds frontend locally and deploys to Pi

set -e

PI_HOST="${1:-raspberrypi.local}"
PI_USER="${2:-bot}"
PROJECT_PATH="/home/$PI_USER/LaserBot"

echo "Building frontend locally..."
cd frontend
VITE_API_BASE_URL=http://localhost:8000 npm run build

echo "Copying built files to Pi..."
rsync -avz --delete dist/ "$PI_USER@$PI_HOST:$PROJECT_PATH/frontend/dist/"

echo "Copying deployment files to Pi..."
rsync -avz deployment/ "$PI_USER@$PI_HOST:$PROJECT_PATH/deployment/"
rsync -avz frontend/Dockerfile.static "$PI_USER@$PI_HOST:$PROJECT_PATH/frontend/"
rsync -avz frontend/nginx.conf "$PI_USER@$PI_HOST:$PROJECT_PATH/frontend/"

echo "Building and starting services on Pi..."
ssh "$PI_USER@$PI_HOST" "cd $PROJECT_PATH && docker compose -f deployment/docker-compose.prod.yml up -d --build"

echo "Deployment complete!"
echo "Frontend: http://$PI_HOST:3000"
echo "Backend: http://$PI_HOST:8000"