from fastapi import FastAPI

from .service import router as service_router
from .db import Base, engine

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Management API")


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(service_router)