# AGENTS

## Stack

| Component | Detail |
|-----------|--------|
| Language  | Python 3.12+ |
| Framework | FastAPI ≥ 0.115 |
| Validation | Pydantic v2 (`pydantic[email]`) |
| Server | Uvicorn |
| Package mgr | uv |
| Tests | pytest + httpx (TestClient) |
| Observability | OpenTelemetry → Jaeger (OTLP HTTP) |

---

## Fast Start

```powershell
uv sync --extra dev          # install all deps
uv run uvicorn app.main:app --reload  # start dev server (http://127.0.0.1:8000)
uv run pytest                # run tests
```

---

## Layer Map

```
app/
├── main.py          — FastAPI instance, router registration, telemetry init
├── store.py         — In-memory state (Dict[int, EmployeeResponse] + counter)
├── telemetry.py     — OTel TracerProvider / MeterProvider / LoggerProvider setup
├── routers/         — One file per resource; HTTP concerns only
└── schemas/         — Pydantic models: Create / Update / Response per resource
tests/
└── test_employees.py
```

---

## Key Conventions

### Schemas
- `Create`: required fields, `Field(...)` validation
- `Update`: all optional (`None` default)
- `Response`: flat, all required, no secrets

### Routers
- `response_model` on every route
- `status.HTTP_*` constants — never hardcode integers
- POST → `HTTP_201_CREATED`; DELETE → `HTTP_204_NO_CONTENT`
- `HTTPException(status_code=status.HTTP_404_NOT_FOUND)` for missing resources
- PUT → `payload.model_dump(exclude_unset=True)` to store

### Tests
- `TestClient` at module level
- `@pytest.fixture(autouse=True)` with `store.reset()` before/after — never share state
- Classes by operation: `TestCreate`, `TestGet`, …
- Assert `response.status_code` and `response.json()` fields

### Observability
- `tracer`/`meter` from `app/telemetry` only — never new providers
- Span names: `"domain.action"` (e.g. `"employee.create"`)
- Jaeger UI: `http://localhost:16686` (`docker compose up -d`)

---

## Skill System

`fastapi-python` skill (`.github/skills/fastapi-python/SKILL.md`) — load before adding routers, schemas, store logic, tests, or OTel spans.

---

## References

- [README.md](README.md) — full feature walkthrough and OTel env vars
- [pyproject.toml](pyproject.toml) — dependency versions
- [docker-compose.yml](docker-compose.yml) — Jaeger setup
