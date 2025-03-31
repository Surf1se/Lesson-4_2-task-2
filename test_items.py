from conftest import BASE_URL
import requests

class TestItems:

    def test_get_items(self, get_items):

        assert isinstance(get_items["data"], list), "Ответ должен быть списком"
        assert len(get_items["data"]) > 0, "Список items не должен быть пустым"

    def test_create_item(self, headers_data, item_data):

        response = requests.post(f"{BASE_URL}/api/v1/items/", json=item_data, headers=headers_data)
        assert response.status_code == 200, "Не удалось создать item"

        incorrect_data = requests.post(f"{BASE_URL}/api/v1/items/", json={"title": 123, "description": 123}, headers=headers_data)
        assert incorrect_data.status_code == 422, "Ожидался код 422 в связи с некорректными данными"

    def test_get_item(self, headers_data, get_items):

        items_list = get_items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        item_id = requests.get(f"{BASE_URL}/api/v1/items/4c6073b8", headers=headers_data)
        assert item_id.status_code == 422, "ID item must  be Guid"

    def test_item_update(self, headers_data, get_items, item_data):

        items_list = get_items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        response = requests.put(f"{BASE_URL}/api/v1/items/{item_id}", json=item_data, headers=headers_data)
        assert response.status_code == 200, "Ошибка обновления item по id"

        incorrect_data = requests.put(f"{BASE_URL}/api/v1/items/{item_id}", json={"title": 123, "description": 123}, headers=headers_data)
        assert incorrect_data.status_code == 422, "Ожидался код 422 при использовании некорректных данных"

    def test_delete_item_by_id(self, headers_data, get_items):

        items_list = get_items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        response = requests.delete(f"{BASE_URL}/api/v1/items/{item_id}", headers=headers_data)
        assert response.status_code == 200, "Ошибка удаления item по id"
