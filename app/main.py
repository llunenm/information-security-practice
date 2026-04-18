from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import auth  # ← Підключаємо роутер аутентифікації

app = FastAPI(
    title="Електронний деканат",
    description="API для управління академічними даними",
    version="0.4.0"
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Електронний деканат API v0.4.0"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables)
    }