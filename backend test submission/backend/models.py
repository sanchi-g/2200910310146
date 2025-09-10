from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(64), unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)