from fastapi import FastAPI

from app.routers import appointment, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(appointment.router)
