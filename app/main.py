from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import DBSessionDep

app = FastAPI()


@app.get("/")
async def root(session: DBSessionDep):
    await session.execute(text("SELECT 1"))
    return {"message": "Hello World"}
