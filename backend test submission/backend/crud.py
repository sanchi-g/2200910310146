from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models
from typing import Optional

def get_by_code(db: Session, code: str):
    return db.query(models.ShortURL).filter(models.ShortURL.short_code == code).first()

def create_short(db: Session, original_url: str, code: str, validity: Optional[int] = None):                 
    expires_at = None
    if validity:
        expires_at = datetime.utcnow() + timedelta(minutes=validity)

    short = models.ShortURL(
        original_url=original_url,
        short_code=code,
        expires_at=expires_at
    )
    db.add(short)
    db.commit()
    db.refresh(short)
    return short

def increment_clicks(db: Session, short):                   #to increment clicks
    short.clicks += 1
    db.commit()
    db.refresh(short)
