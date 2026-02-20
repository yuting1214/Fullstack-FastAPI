import pytest
import time
from fastapi import status

valid_message_data = {"content": "Hello, world!"}
RUN_TIMES = 10


@pytest.mark.anyio
async def test_create_message_bulk(async_client):
    start_time = time.time()
    for _ in range(RUN_TIMES):
        response = await async_client.post("/api/v1/messages/", json=valid_message_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()
    elapsed = time.time() - start_time
    print(f"Async bulk insert of {RUN_TIMES} messages took {elapsed:.3f}s")
