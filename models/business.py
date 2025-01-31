from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from database import Base

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    address = Column(String(255))
    city = Column(String(100))
    country = Column(String(50))
    phone = Column(String(50))
    email = Column(String(100))
    telegramid = Column(String(100))
    website = Column(String(255))
    instagram = Column(String(255))
    facebook = Column(String(255))
    opening_hours = Column(JSON)
    specialties = Column(Text)
    keywords = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


