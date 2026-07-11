import pytest
from fastapi import status

from src.backend.core.config import global_settings


@pytest.mark.anyio
async def test_docs_credentials_never_empty():
    # With no USER_NAME/PASSWORD env vars, credentials are auto-generated —
    # an empty login form must never authenticate.
    assert global_settings.USER_NAME
    assert global_settings.PASSWORD


@pytest.mark.anyio
async def test_login_page_renders(async_client):
    response = await async_client.get("/login")
    assert response.status_code == status.HTTP_200_OK
    assert "login" in response.text.lower()


@pytest.mark.anyio
async def test_login_rejects_empty_credentials(async_client):
    # FastAPI 0.139 rejects empty required form fields with 422; either way,
    # an empty form must never produce the success redirect.
    response = await async_client.post("/login", data={"username": "", "password": ""})
    assert response.status_code != status.HTTP_303_SEE_OTHER


@pytest.mark.anyio
async def test_login_rejects_wrong_credentials(async_client):
    response = await async_client.post(
        "/login", data={"username": "nobody", "password": "wrong-password"}
    )
    assert response.status_code == status.HTTP_200_OK  # login page re-rendered
    assert "Invalid credentials" in response.text


@pytest.mark.anyio
async def test_login_accepts_configured_credentials(async_client):
    response = await async_client.post(
        "/login",
        data={
            "username": global_settings.USER_NAME,
            "password": global_settings.PASSWORD,
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/docs"


@pytest.mark.anyio
async def test_htmx_login_success_sends_client_redirect(async_client):
    response = await async_client.post(
        "/login",
        data={
            "username": global_settings.USER_NAME,
            "password": global_settings.PASSWORD,
        },
        headers={"HX-Request": "true"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["hx-redirect"] == "/docs"


@pytest.mark.anyio
async def test_htmx_login_failure_swaps_card_fragment(async_client):
    response = await async_client.post(
        "/login",
        data={"username": "nobody", "password": "wrong-password"},
        headers={"HX-Request": "true"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Invalid credentials" in response.text
    assert 'id="login-card"' in response.text
    assert "<html" not in response.text  # fragment, not the full page
