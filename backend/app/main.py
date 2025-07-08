from contextlib import asynccontextmanager
from app.routes import robot_routes, training_routes
from app.database_init import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize database on startup
    init_db()
    yield

app = FastAPI(title="LaserBot API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default port
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(robot_routes.router)
app.include_router(training_routes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LaserBot API"}
