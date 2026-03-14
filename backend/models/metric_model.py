from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    cpu = Column(Float)
    memory = Column(Float)
    latency = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)