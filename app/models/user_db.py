from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.calendar_db import CalendarDB

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)

    calendar = relationship("CalendarDB", back_populates="user")
