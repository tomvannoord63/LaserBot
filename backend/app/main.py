import logging
from contextlib import asynccontextmanager
from app.routes import robot_routes, training_routes
from app.database_init import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize database on startup
    init_db()
    yield

app = FastAPI(title="LaserBot API", lifespan=lifespan)

# Configure CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(robot_routes.router)
app.include_router(training_routes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LaserBot API"}
