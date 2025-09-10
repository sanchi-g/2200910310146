from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ShortenRequest(BaseModel): 
    original_url: HttpUrl 
    short_code: Optional[str] = None 
    validity: Optional[int] = None 
class ShortenResponse(BaseModel): 
    short_url: str 
    code: str 
    expires_at: Optional[datetime] = None
