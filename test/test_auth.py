import requests
from src.constant import BASE_URL

class TestAuth:
    def test_auth_session(self, auth_session):
        response = auth_session.get(f"{BASE_URL}/api/v1/users/me")
        assert response.status_code == 200, "Ошибка при получении данных пользователя"
        user_data = response.json()
        assert "email" in user_data, "Поле 'email' отсутствует в ответе"

    def test_token(self, get_auth_token):
        token = get_auth_token
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        assert response.status_code == 200, "Ошибка при получении token"

        test_token_response = requests.post(f"{BASE_URL}/api/v1/login/test-token", headers=headers)
        assert test_token_response.status_code == 200, "token не прошел проверку"

    def test_incorrect_token(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "incorrect_token"
        }
        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        assert response.status_code == 401, "Ожидалась 401 ошибка  при передаче некорректного токена"

    def test_incorrect_cred(self):
        auth_data = {
            "username": "email",
            "password": "password"
        }
        response = requests.post(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
        assert response.status_code == 400, "Ожидалась 400 ошибка  при вводе некорректных кредов"
