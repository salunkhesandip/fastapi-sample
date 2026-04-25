from fastapi import FastAPI
from app.routers import employees

app = FastAPI(
    title="Employee API",
    description="A sample CRUD API built with FastAPI",
    version="1.0.0",
)

app.include_router(employees.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Employee API is running"}
