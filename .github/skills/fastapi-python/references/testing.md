# Testing Patterns

## Setup

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import store

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    store.reset()
    yield
    store.reset()
```

## Example — validation error (hardest case)

```python
class TestCreateEmployee:
    def test_returns_201_with_body(self):
        response = client.post("/employees/", json={
            "name": "Alice", "email": "alice@example.com",
            "department": "Engineering", "salary": 70_000.0,
        })
        assert response.status_code == 201
        assert response.json()["name"] == "Alice"

    def test_invalid_email_returns_422(self):
        response = client.post("/employees/", json={
            "name": "Bob", "email": "not-an-email",
            "department": "IT", "salary": 50_000.0,
        })
        assert response.status_code == 422
```

## Rules

- `autouse=True` fixture resets store — never share state between tests
- Group tests in classes by operation (`TestCreate`, `TestGet`, …)
- Assert status code and response body fields
- Use real store — never mock it
