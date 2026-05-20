import pytest
from fastapi.testclient import TestClient
from pygments.lexers import data

from main import app

client = TestClient(app)

office_data = {
    "country": "Poland",
    "city": "Kraków",
    "street": "Grodzka",
    "number": "12A",
    "phone": "+48501928348"
}

@pytest.fixture
def setup_office():
    """Setup an office object"""

    response = client.post("/office", json=office_data)
    assert response.status_code == 201
    return response.json()

def test_create_employee_success(client, setup_office):
    """Create an employee object"""
    office_id = setup_office[0]["id"]

    employee_data_1 = {
        "name": "Jan",
        "surname": "Kowalski",
        "email": "j.kowalski@example.com",
        "office_id": office_id,
        "salary": "5000"
    }

    response = client.post("/employees", json=employee_data_1)

    assert response.status_code == 201

    data = response.json()

    if isinstance(data, list):
        data = data[0]

    assert data["name"] == "Jan"
    assert data["surname"] == "Kowalski"
    assert data["email"] == "j.kowalski@example.com"
    assert data["office"]["id"] == office_id
    assert "id" in data


def test_get_employees_returns_only_current_test_data(client, setup_office):
    response_empty = client.get("/employees/")
    assert len(response_empty.json()) == 0

    employee_data_2 = {
        "name": "Anna",
        "surname": "Nowak",
        "email": "anna.nowak@example.com",
        "office_id": setup_office[0]["id"],
        "salary": "6000"
    }
    employee_data_1 = {
        "name": "Jan",
        "surname": "Kowalski",
        "email": "j.kowalski@example.com",
        "office_id": setup_office[0]["id"],
        "salary": "5000"
    }

    client.post("/employees/", json=employee_data_1)
    client.post("/employees/", json=employee_data_2)

    response_get = client.get("/employees/")
    assert response_get.status_code == 200
    assert len(response_get.json()) == 2
    assert response_get.json()[0]["name"] == "Jan"
    assert response_get.json()[1]["name"] == "Anna"

def test_get_employees_returns_only_one(client, setup_office):
    """Get a specific employee object"""
    employee_data_2 = {
        "name": "Anna",
        "surname": "Nowak",
        "email": "anna.nowak@example.com",
        "office_id": setup_office[0]["id"],
        "salary": "6000"
    }

    response = client.post("/employees/", json=employee_data_2)
    data = response.json()

    if isinstance(data, list):
        data = data[0]

    response_get = client.get(f"/employees/{data['id']}")

    assert response_get.json()["name"] == "Anna"

def test_delete_employee_success(client, setup_office):
    """Delete an employee object"""
    employee_data_2 = {
        "name": "Anna",
        "surname": "Nowak",
        "email": "anna.nowak@example.com",
        "office_id": setup_office[0]["id"],
        "salary": "6000"
    }

    response = client.post("/employees/", json=employee_data_2)
    assert response.status_code == 201

    data = response.json()
    if isinstance(data, list):
        data = data[0]

    delete_response = client.delete(f"/employees/{data['id']}")
    assert delete_response.status_code == 204

def test_patch_employee_success(client, setup_office):
    """Patch an employee object"""
    employee_data_2 = {
        "name": "Anna",
        "surname": "Nowak",
        "email": "anna.nowak@example.com",
        "office_id": setup_office[0]["id"],
        "salary": "6000"
    }

    response = client.post("/employees/", json=employee_data_2)
    assert response.status_code == 201

    data = response.json()
    if isinstance(data, list):
        data = data[0]

    patch_response = client.patch(f"/employees/{data['id']}", json={"name": "Krystyna"})
    assert patch_response.status_code == 200
    assert patch_response.json()["name"] == "Krystyna"


def test_get_non_existent_employee():
    """Get a non-existent employee object"""
    random_uuid = "4d2a13b6-9817-4933-90d5-123456789abc"
    response = client.get(f"/employees/{random_uuid}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

