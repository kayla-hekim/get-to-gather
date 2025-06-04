from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    summary = Column(String(200), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(String(200))
    location = Column(String(200))
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
