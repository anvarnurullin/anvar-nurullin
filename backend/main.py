from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn
from typing import List
from pydantic import BaseModel

from database import get_db, engine, Base
from models import City

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://77.238.250.76",
        "http://anvar-nurullin.ru"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/message")
def message():
    return "Люблю только Арину❤️"

@app.get("/db-ping")
def db_ping(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version();")).scalar()
    return {"postgres_version": version}

class CityCreate(BaseModel):
    name: str

class CityRead(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/cities", response_model=List[CityRead])
def list_cities(db: Session = Depends(get_db)):
    return db.execute(select(City)).scalars().all()

@app.post("/cities", response_model=CityRead, status_code=201)
def create_city(payload: CityCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name is required")
    exists = db.execute(select(City).where(City.name == name)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="City already exists")
    city = City(name=name)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.execute(select(City).where(City.id == city_id)).scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
