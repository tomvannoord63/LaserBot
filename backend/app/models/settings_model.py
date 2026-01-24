from app.database import Base
from sqlalchemy import Column, Integer, String


class SettingsModel(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
