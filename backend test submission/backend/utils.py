import string, secrets
from sqlalchemy.orm import Session
from .models import ShortURL

ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int = 6) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def generate_unique_code(db: Session, length: int = 6) -> str:
    # simple loop to avoid collisions
    while True:
        code = generate_code(length)
        exists = db.query(ShortURL).filter(ShortURL.short_code == code).first()
        if not exists:
            return code
