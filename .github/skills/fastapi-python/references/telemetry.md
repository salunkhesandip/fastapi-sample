# OpenTelemetry Instrumentation

## Example — tracing a route

```python
from app.telemetry import tracer

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate):
    with tracer.start_as_current_span("employee.create") as span:
        span.set_attribute("employee.department", payload.department)
        result = store.create(payload.model_dump())
        span.set_attribute("employee.id", result.id)
        return result
```

## Rules

- `tracer`/`meter` from `app/telemetry` only — never new providers
- Span names: `"domain.action"` (e.g. `"employee.create"`)
- `start_as_current_span` as context manager — handles start/end/exception
- `span.set_attribute(...)` for Jaeger filtering

## NOT FOR

- Configuring exporters or providers — edit `app/telemetry.py` directly
