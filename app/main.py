from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import auth, students, teachers, admin  

app = FastAPI(
    title="Електронний деканат",
    description="API для управління академічними даними",
    version="0.5.0"
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Електронний деканат API v0.5.0"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables)
    }