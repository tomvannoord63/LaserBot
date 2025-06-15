# LaserBot

This project is a laser pointer robot that is a 2-axis gimbal with a laser diode attached to the end of the robot. The project is based around the JJRobots laser pointer robot. The system consists of a React frontend and FastAPI backend, both running on a Raspberry Pi.

## Project Structure

```
LaserBot/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   └── requirements.txt
└── frontend/         # React frontend
    ├── src/          # Source code
    └── package.json
```

## Prerequisites

- Raspberry Pi (tested on Raspberry Pi Zero W)
- Python 3.11+
- Node.js 16+
- npm or yarn

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install poetry
   poetry install --no-root
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The frontend will be available at `http://localhost:5173`

## Development

### Backend Development
- The FastAPI backend provides RESTful endpoints for controlling the laser pointer
- API documentation is available at `http://localhost:8000/docs`
- Main application code is in `backend/app/main.py`

### Frontend Development
- React frontend provides a user interface for controlling the laser pointer
- Main application code is in `frontend/src/App.js`
- API service calls are in `frontend/src/services/`

## Production Deployment

For production deployment on the Raspberry Pi:

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   # or
   yarn build
   ```

2. Configure the backend to serve the frontend static files
3. Set up the backend as a system service using systemd
4. Configure the Raspberry Pi to start the service on boot

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
