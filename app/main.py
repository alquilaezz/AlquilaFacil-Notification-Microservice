from fastapi import FastAPI
from .database import Base, engine
from .routers import notification

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notification Service")

app.include_router(notification.router)
