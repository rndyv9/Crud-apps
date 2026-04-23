"""
API tests for the Contact CRUD app.

Each test starts with a clean database (see the `reset_db` fixture) so
they can run independently and in any order.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before every test for isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------- helpers ----------

def create_contact(name: str, phone: str):
    return client.post("/contact", params={"name": name, "phone": phone})


def get_contacts():
    return client.get("/contacts").json()


def find_contact(name: str):
    return next((c for c in get_contacts() if c["name"] == name), None)


# ---------- create ----------

class TestCreateContact:
    def test_create_returns_created_message(self):
        response = create_contact("John", "123")

        assert response.status_code == 200
        assert response.json() == {"message": "created"}

    def test_created_contact_appears_in_list(self):
        create_contact("John", "123")

        contact = find_contact("John")
        assert contact is not None
        assert contact["phone_number"] == "123"

    def test_creating_same_name_same_phone_returns_no_change(self):
        create_contact("John", "123")

        response = create_contact("John", "123")

        assert response.status_code == 200
        assert response.json() == {"message": "no change"}

    def test_can_create_multiple_distinct_contacts(self):
        create_contact("John", "123")
        create_contact("Jane", "456")

        contacts = get_contacts()
        names = sorted(c["name"] for c in contacts)
        assert names == ["Jane", "John"]


# ---------- update ----------

class TestUpdateContact:
    def test_update_changes_phone_number(self):
        create_contact("John", "123")

        response = create_contact("John", "222")

        assert response.status_code == 200
        assert response.json() == {"message": "updated"}
        assert find_contact("John")["phone_number"] == "222"

    def test_update_does_not_create_duplicate(self):
        create_contact("John", "123")
        create_contact("John", "222")

        contacts = [c for c in get_contacts() if c["name"] == "John"]
        assert len(contacts) == 1


# ---------- delete ----------

class TestDeleteContact:
    def test_delete_existing_contact(self):
        create_contact("John", "123")

        response = client.delete("/contact/John")

        assert response.status_code == 200
        assert response.json() == {"message": "deleted"}
        assert find_contact("John") is None

    def test_delete_missing_contact_returns_not_found(self):
        response = client.delete("/contact/Ghost")

        assert response.status_code == 200
        assert response.json() == {"message": "not found"}


# ---------- read ----------

class TestListContacts:
    def test_empty_list_when_no_contacts(self):
        assert get_contacts() == []

    def test_list_returns_all_contacts(self):
        create_contact("John", "123")
        create_contact("Jane", "456")

        contacts = get_contacts()
        assert len(contacts) == 2


# ---------- export ----------

class TestExportCsv:
    def test_csv_headers_and_content_type(self):
        create_contact("John", "123")

        response = client.get("/export/csv")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/csv")
        assert "attachment" in response.headers["content-disposition"]

    def test_csv_contains_contact_rows(self):
        create_contact("John", "123")
        create_contact("Jane", "456")

        body = client.get("/export/csv").text
        lines = [line for line in body.strip().splitlines() if line]

        assert lines[0] == "name,phone_number"
        assert "John,123" in lines
        assert "Jane,456" in lines


# ---------- parametrized example ----------

@pytest.mark.parametrize("name,phone", [
    ("Alice", "111"),
    ("Bob", "222"),
    ("Charlie", "333"),
])
def test_create_multiple_contacts_parametrized(name, phone):
    response = create_contact(name, phone)

    assert response.status_code == 200
    assert find_contact(name)["phone_number"] == phone
