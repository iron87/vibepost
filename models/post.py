from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime
from database import Base

# TODO: we can decouple the database model from the core model  


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'))
    content = Column(Text, nullable=False)
    image_url = Column(Text)
    status = Column(String(50), default='draft')
    scheduled_for = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)