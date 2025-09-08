from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn

from database import get_db

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
