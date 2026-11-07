from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from db import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    predicted_genre = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())