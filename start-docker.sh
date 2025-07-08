#!/bin/bash

# LaserBot Docker Development Setup

echo "🤖 Starting LaserBot Docker Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start the frontend container
echo "🏗️  Building and starting frontend container..."
docker-compose up --build -d

# Wait a moment for the container to start
sleep 3

# Show container status
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo ""
echo "To stop the containers, run:"
echo "  docker-compose down"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f frontend"
echo ""
echo "To rebuild after changes:"
echo "  docker-compose up --build"