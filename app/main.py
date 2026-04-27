from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.routers import employees
from app.telemetry import setup_telemetry

setup_telemetry()

app = FastAPI(
    title="Employee API",
    description="A sample CRUD API built with FastAPI",
    version="1.0.0",
)

app.include_router(employees.router)

FastAPIInstrumentor.instrument_app(app)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Employee API is running"}
