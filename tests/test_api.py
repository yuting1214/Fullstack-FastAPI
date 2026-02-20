import pytest
from fastapi import status

valid_message_data = {"content": "Hello, world!"}
invalid_message_data = {"invalid_field": "This should fail"}


@pytest.mark.anyio
async def test_create_message(async_client):
    response = await async_client.post("/api/v1/messages/", json=valid_message_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["content"] == valid_message_data["content"]
    assert "id" in data


@pytest.mark.anyio
async def test_create_message_invalid_data(async_client):
    response = await async_client.post("/api/v1/messages/", json=invalid_message_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.anyio
async def test_get_messages(async_client):
    await async_client.post("/api/v1/messages/", json=valid_message_data)
    response = await async_client.get("/api/v1/messages/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.anyio
async def test_get_message(async_client):
    create_response = await async_client.post("/api/v1/messages/", json=valid_message_data)
    message_id = create_response.json()["id"]
    response = await async_client.get(f"/api/v1/messages/{message_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == message_id
    assert data["content"] == valid_message_data["content"]


@pytest.mark.anyio
async def test_update_message(async_client):
    create_response = await async_client.post("/api/v1/messages/", json=valid_message_data)
    message_id = create_response.json()["id"]
    updated_data = {"content": "Updated content"}
    response = await async_client.put(f"/api/v1/messages/{message_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["content"] == updated_data["content"]


@pytest.mark.anyio
async def test_delete_message(async_client):
    create_response = await async_client.post("/api/v1/messages/", json=valid_message_data)
    message_id = create_response.json()["id"]
    delete_response = await async_client.delete(f"/api/v1/messages/{message_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    get_response = await async_client.get(f"/api/v1/messages/{message_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
