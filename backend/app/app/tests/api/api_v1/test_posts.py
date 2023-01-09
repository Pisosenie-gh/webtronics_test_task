from sqlalchemy.orm import Session

from app.core.config import settings

from fastapi.testclient import TestClient

def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/posts/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/posts/", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content[0]["title"] is not None
    assert content[0]["description"] is not None
    assert content[0]["id"] is not None

def test_update_post(client: TestClient, superuser_token_headers: dict
)-> None:
    # Создание поста
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/posts/", headers=superuser_token_headers, json=data,
    )
    post_id = response.json()["id"]
    assert response.status_code == 200
    # Обновление поста
    updated_data = {"title": "Updated Title", "description": "Updated Body"}
    response = client.put(f"{settings.API_V1_STR}/posts/{post_id}", headers=superuser_token_headers, json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["description"] == "Updated Body"



def test_delete_post(client: TestClient, superuser_token_headers: dict):
    data = {"title": "Foo", "description": "Fighters"}
    post = client.post(
        f"{settings.API_V1_STR}/posts/", headers=superuser_token_headers, json=data,
    )
    post_id = post.json()["id"]

    response = client.delete(f"{settings.API_V1_STR}/posts/{post_id}", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == post.json()

    # try to delete a non-existent post
    response = client.delete(f"{settings.API_V1_STR}/posts/999", headers=superuser_token_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Пост не найден"





