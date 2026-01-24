from app.database import SessionLocal, engine
from app.models.position_model import PositionModel
from app.models.settings_model import SettingsModel
from app.position_manager import Position  # Import the Pydantic model for initial data


def init_db():
    """Initialize the database with tables and default data."""
    # Create all tables
    PositionModel.metadata.create_all(bind=engine)
    SettingsModel.metadata.create_all(bind=engine)

    # Initialize default settings
    from app.settings_manager import settings_manager
    settings_manager.ensure_defaults()

    # Check if we already have data
    db = SessionLocal()
    try:
        existing_positions = db.query(PositionModel).count()
        if existing_positions == 0:
            # Add default positions
            default_positions = [
                PositionModel(
                    id="position_1",
                    x=0,
                    y=-16,
                    name="Room Center",
                    description="Room center position",
                ),
                PositionModel(
                    id="position_2",
                    x=80,
                    y=-52,
                    name="Right of TV",
                    description="Forward and right position",
                ),
                PositionModel(
                    id="position_3",
                    x=-77,
                    y=-91,
                    name="Far Left",
                    description="Back and left position",
                ),
                PositionModel(
                    id="position_4",
                    x=-77,
                    y=-75,
                    name="By 3D Printer",
                    description="Back center position",
                ),
                PositionModel(
                    id="position_5",
                    x=-63,
                    y=-38,
                    name="Water Pump",
                    description="Mid back position",
                ),
                PositionModel(
                    id="position_6",
                    x=-40,
                    y=-70,
                    name="Center Square 1",
                    description="Center square 1 position",
                ),
                PositionModel(
                    id="position_7",
                    x=0,
                    y=0,
                    name="Home Position",
                    description="Default home position for the robot",
                ),
                PositionModel(
                    id="position_8",
                    x=-40,
                    y=-45,
                    name="Center Square 2",
                    description="Center square 2 position",
                ),
                PositionModel(
                    id="position_9",
                    x=0,
                    y=-30,
                    name="Center Square 3",
                    description="Center square 3 position",
                ),
                PositionModel(
                    id="position_10",
                    x=0,
                    y=-70,
                    name="Center Square 4",
                    description="Center square 4 position",
                ),
            ]

            db.add_all(default_positions)
            db.commit()
            print("Database initialized with default positions")
        else:
            print("Database already contains data, skipping initialization")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
