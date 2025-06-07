from app.routes import robot_routes, training_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LaserBot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
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
