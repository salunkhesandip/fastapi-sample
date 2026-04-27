# fastapi-sample

A sample CRUD REST API built with [FastAPI](https://fastapi.tiangolo.com/), using an in-memory store.

## Features

- Full CRUD for an `Employee` resource
- Input validation with Pydantic v2
- Auto-generated interactive docs (Swagger UI & ReDoc)
- Test suite with `pytest` and FastAPI's `TestClient`

## Project Structure

```
fastapi-sample/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── store.py             # In-memory data store
│   ├── telemetry.py         # OpenTelemetry setup (traces, metrics, logs)
│   ├── schemas/
│   │   └── employee.py      # Pydantic request/response models
│   └── routers/
│       └── employees.py     # Employee CRUD endpoints
├── tests/
│   └── test_employees.py    # Test suite
├── docker-compose.yml       # Jaeger for local observability
├── pyproject.toml           # Project metadata & dependencies (uv)
└── .gitignore
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — install with:
  ```bash
  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Getting Started

```bash
# Enter the project
cd fastapi-sample

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Sync dependencies and create virtual environment
uv sync --extra dev

# Run the development server
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Docs

Once the server is running, access the interactive documentation at:

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/docs` | Swagger UI (interactive - try endpoints here) |
| `http://127.0.0.1:8000/redoc` | ReDoc (alternative documentation) |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/employees/` | List all employees |
| `GET` | `/employees/{id}` | Get employee by ID |
| `POST` | `/employees/` | Create a new employee |
| `PUT` | `/employees/{id}` | Update an employee (partial) |
| `DELETE` | `/employees/{id}` | Delete an employee |

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "email": "alice@example.com", "department": "Engineering", "salary": 75000}'
```

## Running Tests

Once dependencies are installed via `uv sync --extra dev`, run tests with:

```bash
uv run pytest
```

## Dependency Management

Dependencies are declared in `pyproject.toml` and managed by `uv`:

```bash
uv sync --extra dev      # Install all dependencies (dev included)
uv add <package>         # Add a runtime dependency
uv add --dev <package>   # Add a dev dependency
uv remove <package>      # Remove a dependency
uv lock                  # Regenerate the lockfile
```

## Observability (OpenTelemetry + Jaeger)

The app is instrumented with [OpenTelemetry](https://opentelemetry.io/) and exports **traces**, **metrics**, and **logs** to any OTLP-compatible backend.

### How it works

| File | Role |
|------|------|
| `app/telemetry.py` | Bootstraps TracerProvider, MeterProvider, and LoggerProvider |
| `app/main.py` | Calls `setup_telemetry()` at startup, then auto-instruments FastAPI with `FastAPIInstrumentor` |

Every inbound HTTP request automatically gets a trace with span attributes (method, route, status code). Trace/span IDs are injected into every log line.

### Running Jaeger locally

**Step 1 — Start Jaeger** (requires Docker):

```bash
docker compose up -d
```

This starts `jaegertracing/all-in-one` with OTLP enabled:

| Port | Purpose |
|------|---------|
| `4318` | OTLP HTTP — the app sends traces here |
| `4317` | OTLP gRPC (alternative) |
| `16686` | Jaeger UI |

**Step 2 — Start the API** (in a separate terminal):

```bash
uv run uvicorn app.main:app --reload
```

**Step 3 — Generate some traffic**:

```bash
curl http://127.0.0.1:8000/
curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "email": "alice@example.com", "department": "Engineering", "salary": 75000}'
curl http://127.0.0.1:8000/employees/
```

**Step 4 — View traces in Jaeger UI**:

Open `http://localhost:16686` in your browser.

1. Select **`fastapi-sample`** from the *Service* dropdown.
2. Click **Find Traces**.
3. Click any trace to inspect spans, tags, and timing.

### Environment variables

All configuration is via environment variables — no code changes needed to switch backends:

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_SERVICE_NAME` | `fastapi-sample` | Service name shown in Jaeger |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318` | OTLP HTTP collector base URL |
| `SERVICE_VERSION` | `1.0.0` | `service.version` resource attribute |
| `DEPLOYMENT_ENV` | `local` | `deployment.environment` resource attribute |

Example — pointing to a remote collector:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 \
OTEL_SERVICE_NAME=fastapi-sample \
uv run uvicorn app.main:app
```

### Stopping Jaeger

```bash
docker compose down
```
