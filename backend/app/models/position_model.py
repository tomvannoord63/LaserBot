from app.database import Base
from sqlalchemy import Column, Float, String


class PositionModel(Base):
    __tablename__ = "positions"

    id = Column(String, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default="")
