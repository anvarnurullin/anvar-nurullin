from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://77.238.250.76"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/message")
def message():
    return "Люблю только Арину❤️"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)