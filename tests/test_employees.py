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


def _create_employee(name="Alice", email="alice@example.com", department="Engineering", salary=70000.0):
    return client.post("/employees/", json={
        "name": name,
        "email": email,
        "department": department,
        "salary": salary,
    })


class TestHealthCheck:
    def test_root_returns_ok(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestCreateEmployee:
    def test_create_returns_201(self):
        response = _create_employee()
        assert response.status_code == 201

    def test_create_returns_employee_with_id(self):
        response = _create_employee()
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert data["department"] == "Engineering"
        assert data["salary"] == 70000.0

    def test_create_with_invalid_email_returns_422(self):
        response = client.post("/employees/", json={
            "name": "Bob",
            "email": "not-an-email",
            "department": "HR",
            "salary": 50000.0,
        })
        assert response.status_code == 422

    def test_create_with_negative_salary_returns_422(self):
        response = client.post("/employees/", json={
            "name": "Carol",
            "email": "carol@example.com",
            "department": "Finance",
            "salary": -100.0,
        })
        assert response.status_code == 422


class TestGetEmployee:
    def test_get_all_returns_empty_list(self):
        response = client.get("/employees/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_returns_created_employees(self):
        _create_employee("Alice", "alice@example.com")
        _create_employee("Bob", "bob@example.com")
        response = client.get("/employees/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_by_id_returns_employee(self):
        _create_employee()
        response = client.get("/employees/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Alice"

    def test_get_by_id_returns_404_when_not_found(self):
        response = client.get("/employees/999")
        assert response.status_code == 404


class TestUpdateEmployee:
    def test_update_returns_updated_employee(self):
        _create_employee()
        response = client.put("/employees/1", json={"salary": 90000.0})
        assert response.status_code == 200
        assert response.json()["salary"] == 90000.0

    def test_update_partial_fields_only(self):
        _create_employee()
        response = client.put("/employees/1", json={"department": "Management"})
        data = response.json()
        assert data["department"] == "Management"
        assert data["name"] == "Alice"

    def test_update_returns_404_when_not_found(self):
        response = client.put("/employees/999", json={"salary": 90000.0})
        assert response.status_code == 404


class TestDeleteEmployee:
    def test_delete_returns_204(self):
        _create_employee()
        response = client.delete("/employees/1")
        assert response.status_code == 204

    def test_delete_removes_employee(self):
        _create_employee()
        client.delete("/employees/1")
        response = client.get("/employees/1")
        assert response.status_code == 404

    def test_delete_returns_404_when_not_found(self):
        response = client.delete("/employees/999")
        assert response.status_code == 404
