# LaserBot

A laser pointer robot system featuring a 2-axis gimbal with integrated laser diode, based on the JJRobots laser pointer platform. The system combines a React TypeScript frontend with a FastAPI backend, designed for deployment on Raspberry Pi hardware.

## Project Structure

```
LaserBot/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application code
│   │   ├── main.py           # FastAPI app with CORS configuration
│   │   ├── database.py       # SQLAlchemy database configuration
│   │   ├── position_manager.py # Position sequence management
│   │   ├── robot.py          # Robot interface module
│   │   ├── models/           # Database models
│   │   ├── routes/           # API route definitions
│   │   └── services/         # Business logic services
│   ├── pyproject.toml        # uv/Python dependencies
│   └── data/                 # SQLite database storage
├── frontend/                  # React TypeScript frontend
│   ├── src/                  # Source code
│   │   ├── App.tsx          # Main application component
│   │   ├── pages/           # Route components (Dashboard, Training)
│   │   ├── components/      # Reusable UI components
│   │   ├── services/        # API client (robotApi.ts)
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript type definitions
│   ├── package.json         # npm dependencies
│   └── dist/                # Production build output
├── robot/                     # Hardware control module
│   ├── control.py            # LaserRobot UDP communication class
│   └── firmware/             # ESP8266 firmware and documentation
└── deployment/                # Production deployment files
    ├── INSTALL.md           # Raspberry Pi installation guide
    ├── deploy.sh            # Automated deployment script
    ├── docker-compose.prod.yml # Production Docker configuration
    └── laserbot-backend.service # Systemd service configuration
```

## Prerequisites

- **Hardware**: Raspberry Pi (tested on Raspberry Pi Zero W) with JJRobots laser pointer robot
- **Software**: 
  - Python 3.11+
  - Node.js 18+
  - uv (Python package manager)
  - Docker & Docker Compose (for containerized deployment)

## Quick Start (Development)

### Backend Setup

1. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   uv sync
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to set ROBOT_IP_ADDRESS=<your-robot-ip>
   ```

3. Run the development server:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`

### Frontend Setup

1. Navigate to the frontend directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Development Workflow

### Backend Development
- **FastAPI Backend**: RESTful API with automatic OpenAPI documentation
- **Database**: SQLite with SQLAlchemy ORM for position storage
- **Robot Control**: UDP socket communication with ESP8266-based hardware
- **Key Files**:
  - `backend/app/main.py` - FastAPI application entry point
  - `backend/app/routes/robot_routes.py` - Robot control endpoints
  - `backend/robot/control.py` - Hardware communication layer

### Frontend Development
- **React + TypeScript**: Modern React with full TypeScript support
- **Routing**: React Router with Dashboard and Training pages
- **Styling**: Tailwind CSS with Lucide React icons
- **API Integration**: Centralized API client in `frontend/src/services/robotApi.ts`
- **State Management**: React hooks with custom useRobotStatus hook

### Development Commands

```bash
# Backend
cd backend
uv run black .              # Format Python code
uv run isort .              # Sort imports
uv run pytest              # Run tests

# Frontend
cd frontend
npm run lint                # Run ESLint
npm run build               # Production build
```

### Docker Development
For containerized frontend development:

1. Start backend natively:
   ```bash
   cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start frontend in Docker:
   ```bash
   docker-compose up --build
   ```

## Production Deployment

For production deployment on Raspberry Pi, see the detailed [Installation Guide](deployment/INSTALL.md).

### Quick Production Setup
1. Use the automated deployment script:
   ```bash
   ./deployment/deploy.sh raspberrypi.local bot
   ```

2. Or follow manual deployment steps in `deployment/INSTALL.md`

### Architecture Overview
- **Backend**: FastAPI with systemd service management
- **Frontend**: Dockerized nginx serving static React build
- **Database**: SQLite with automatic initialization
- **Hardware**: UDP communication with ESP8266-based robot controller

## API Features

- **Robot Control**: Move laser pointer, enable/disable laser
- **Position Management**: Save, recall, and sequence laser positions
- **Training Mode**: Interactive position recording and playback
- **Real-time Status**: WebSocket-style status updates via REST polling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
