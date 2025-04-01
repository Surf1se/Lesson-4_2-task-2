from constant import BASE_URL, HEADERS
import pytest
import requests
from faker import Faker

fake = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    passData = {
        "username": "andrei@yandex.ru",
        "password": "Qwerty44!"
    }

    auth_response = session.post(f"{BASE_URL}/api/v1/login/access-token", data = passData)
    assert auth_response.status_code == 200

    token = auth_response.json().get("access_token")
    assert token is not None

    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture()
def get_auth_token():
    auth_data = {
        "username": "andrei@yandex.ru",
        "password": "Qwerty44!"
    }
    response = requests.post(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
    assert response.status_code == 200

    return response.json().get("access_token")

@pytest.fixture()
def headers_data(get_auth_token):
    token = get_auth_token
    return  {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

@pytest.fixture()
def item_data():
    return {
  "title": fake.word(),
  "description": fake.text()
}

@pytest.fixture()
def get_items(headers_data):
    headers = headers_data

    response = requests.get(f"{BASE_URL}/api/v1/items/", headers=headers)
    assert response.status_code == 200, "Список items не получен"

    items = response.json()
    return items
