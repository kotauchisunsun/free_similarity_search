import fastapi
import os
from database import Database

DATABASE_PATH = os.getenv("DATABASE_PATH")

db = Database(DATABASE_PATH)
app = fastapi.FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(query:str):
    return db.query(query)
