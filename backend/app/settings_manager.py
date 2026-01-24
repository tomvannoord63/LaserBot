import logging
from typing import Dict

from app.database import SessionLocal
from app.models.settings_model import SettingsModel

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manager for robot settings stored in the database."""

    DEFAULT_SPEED = 50
    DEFAULT_ACCELERATION = 70

    def __init__(self):
        """Initialize the settings manager."""
        pass

    def _get_db(self):
        """Get a database session."""
        try:
            return SessionLocal()
        except Exception as e:
            logger.error(f"Error creating database session: {str(e)}")
            raise

    def ensure_defaults(self):
        """Ensure default settings exist in the database. Called by init_db()."""
        db = self._get_db()
        try:
            # Check if speed setting exists
            speed_setting = db.query(SettingsModel).filter(SettingsModel.key == "speed").first()
            if not speed_setting:
                logger.info("Creating default speed setting")
                db.add(SettingsModel(key="speed", value=self.DEFAULT_SPEED))

            # Check if acceleration setting exists
            accel_setting = db.query(SettingsModel).filter(SettingsModel.key == "acceleration").first()
            if not accel_setting:
                logger.info("Creating default acceleration setting")
                db.add(SettingsModel(key="acceleration", value=self.DEFAULT_ACCELERATION))

            db.commit()
        except Exception as e:
            logger.error(f"Error ensuring default settings: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def get_settings(self) -> Dict[str, int]:
        """Get all settings from the database."""
        db = self._get_db()
        try:
            settings = db.query(SettingsModel).all()
            return {setting.key: setting.value for setting in settings}
        except Exception as e:
            logger.error(f"Error fetching settings: {str(e)}")
            raise
        finally:
            db.close()

    def update_setting(self, key: str, value: int) -> None:
        """Update a specific setting in the database."""
        db = self._get_db()
        try:
            setting = db.query(SettingsModel).filter(SettingsModel.key == key).first()
            if setting:
                setting.value = value
                db.commit()
                logger.info(f"Updated setting {key} to {value}")
            else:
                logger.warning(f"Setting {key} not found, creating it")
                db.add(SettingsModel(key=key, value=value))
                db.commit()
        except Exception as e:
            logger.error(f"Error updating setting {key}: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    def update_speed_settings(self, speed: int, acceleration: int) -> None:
        """Update both speed and acceleration settings."""
        self.update_setting("speed", speed)
        self.update_setting("acceleration", acceleration)
        logger.info(f"Updated speed settings: speed={speed}, acceleration={acceleration}")


# Create a singleton instance
settings_manager = SettingsManager()
