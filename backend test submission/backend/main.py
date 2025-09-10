import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta

from . import database, models, schemas, crud, utils

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")                          #setting up our base url

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="URL Shortener")

def get_db():                                                                       #to get database
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten/", response_model=schemas.ShortenResponse)                       #this is the post API to get the shortened url
async def shorten(data: schemas.ShortenRequest, db: Session = Depends(get_db)):
    if data.short_code:
        if crud.get_by_code(db, data.short_code):
            raise HTTPException(status_code=400, detail="Short code already exists")              #to check for duplicate codes(if sent by mistake)
        code = data.short_code
    else:
        code = utils.generate_unique_code(db)

    short = crud.create_short(
        db,
        original_url=str(data.original_url),
        code=code,
        validity=data.validity 
    )


    return {
        "short_url": f"{BASE_URL}/{short.short_code}",
        "code": short.short_code,
        "expires_at": short.expires_at
    }

@app.get("/{code}")                                                                  #get API to get no. of clicks and to 
async def redirect(code: str, db: Session = Depends(get_db)):
    short = crud.get_by_code(db, code)
    if not short:
        raise HTTPException(status_code=404, detail="URL not found")

    if short.expires_at and datetime.utcnow() > short.expires_at:
        raise HTTPException(status_code=410, detail="This link has expired")

    crud.increment_clicks(db, short)
    return RedirectResponse(url=short.original_url, status_code=302)
