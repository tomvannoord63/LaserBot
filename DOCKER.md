# LaserBot Docker Setup

This setup allows you to run the frontend in a Docker container with Node.js 18 while keeping the backend running natively on your system.

## Prerequisites

- Docker and Docker Compose installed
- Backend dependencies installed (Poetry)

## Quick Start

1. **Start the backend** (in one terminal):
   ```bash
   cd backend
   poetry install --no-root
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   # Option 1: Use the helper script
   ./start-docker.sh
   
   # Option 2: Use Docker Compose directly
   docker-compose up --build
   ```

3. **Access the applications**:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000

## Development Workflow

- The frontend source code is mounted as a volume, so changes are reflected immediately
- The container will rebuild automatically when you change files
- Backend runs natively on your system with your existing Node.js v11.15.0

## Docker Commands

```bash
# Start containers
docker-compose up

# Start containers in background
docker-compose up -d

# Rebuild containers
docker-compose up --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f frontend

# Access container shell
docker-compose exec frontend sh
```

## Troubleshooting

- **Container can't reach backend**: Make sure the backend is running on `0.0.0.0:8000`, not just `localhost:8000`
- **Permission issues**: Make sure Docker has access to the project directory
- **Port conflicts**: Make sure ports 5173 and 8000 are not in use by other applications

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your System                             │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │            Docker Container                 │               │
│  │                                             │               │
│  │  ┌─────────────────────────────────────────┐ │               │
│  │  │    Frontend (React + Vite)             │ │               │
│  │  │    Node.js 18                          │ │               │
│  │  │    Port: 5173                          │ │               │
│  │  └─────────────────────────────────────────┘ │               │
│  └─────────────────────────────────────────────┘               │
│                         │                                       │
│                         │ API calls                             │
│                         │                                       │
│  ┌─────────────────────────────────────────────┐               │
│  │           Backend (FastAPI)                 │               │
│  │           Native Python                     │               │
│  │           Port: 8000                        │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```