# test_user_Majd_Ayash.py
import pytest
from flask import json

import app as user_app
from app import (app, initial_users, create_db_table, insert_user, get_users,
                 get_user_by_id, update_user, delete_user)

new_user = {
    "name": "Nour Saad",
    "email": "noursaad@gmail.com",
    "phone": "03111222",
    "address": "Verdun Street, Beirut",
    "country": "Lebanon"
}


def without_id(user):
    '''Returns a copy of the user without its user_id'''
    return {key: value for key, value in user.items() if key != "user_id"}


@pytest.fixture(autouse=True)
def database(tmp_path, monkeypatch):
    '''Runs every test against a fresh database file, the same as a first run of the app'''
    monkeypatch.setattr(user_app, "DATABASE", str(tmp_path / "test_database.db"))
    create_db_table()


@pytest.fixture
def client():
    return app.test_client()


# 1. The database is created with the specified users when first running the app
def test_database_created_with_initial_users():
    users = get_users()
    assert len(users) == len(initial_users)
    assert [without_id(user) for user in users] == initial_users


def test_initial_users_not_duplicated_on_second_run():
    create_db_table()
    assert len(get_users()) == len(initial_users)


# 2. insert_user()
def test_insert_user():
    inserted = insert_user(new_user)
    assert inserted["user_id"] == len(initial_users) + 1
    assert without_id(inserted) == new_user
    assert len(get_users()) == len(initial_users) + 1


# 3. get_users()
def test_get_users():
    insert_user(new_user)
    users = get_users()
    assert len(users) == len(initial_users) + 1
    assert users[-1]["name"] == "Nour Saad"
    assert all("user_id" in user for user in users)


# 4. get_user_by_id()
def test_get_user_by_id():
    user = get_user_by_id(2)
    assert user["user_id"] == 2
    assert without_id(user) == initial_users[1]


def test_get_user_by_id_not_found():
    assert get_user_by_id(999) == {}


# 5. update_user()
def test_update_user():
    user = get_user_by_id(1)
    user["email"] = "john.doe@outlook.com"
    user["country"] = "Germany"
    updated = update_user(user)
    assert updated == user
    assert get_user_by_id(1)["country"] == "Germany"


# 6. delete_user()
def test_delete_user():
    message = delete_user(3)
    assert message == {"status": "User deleted successfully"}
    assert get_user_by_id(3) == {}
    assert len(get_users()) == len(initial_users) - 1


# api_get_users() - GET /api/users
def test_api_get_users(client):
    response = client.get('/api/users')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data) == len(initial_users)
    assert "Majd Ayash" in str(response.data)


# 7. api_get_user() - GET /api/users/<user_id>
def test_api_get_user(client):
    response = client.get('/api/users/2')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["user_id"] == 2
    assert without_id(data) == initial_users[1]


# 8. api_add_user() - POST /api/users/add
def test_api_add_user(client):
    response = client.post(
        '/api/users/add',
        data=json.dumps(new_user),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["user_id"] == len(initial_users) + 1
    assert without_id(data) == new_user
    assert get_user_by_id(data["user_id"]) == data


# 9. api_update_user() - PUT /api/users/update
def test_api_update_user(client):
    user = get_user_by_id(2)
    user["phone"] = "71999888"
    user["address"] = "Makdessi Street, Beirut"
    response = client.put(
        '/api/users/update',
        data=json.dumps(user),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data == user
    assert get_user_by_id(2) == user


# 10. api_delete_user() - DELETE /api/users/delete/<user_id>
def test_api_delete_user(client):
    response = client.delete('/api/users/delete/1')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data == {"status": "User deleted successfully"}
    assert get_user_by_id(1) == {}
    assert len(get_users()) == len(initial_users) - 1
