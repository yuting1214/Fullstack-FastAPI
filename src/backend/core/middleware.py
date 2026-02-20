from starlette.types import ASGIApp, Scope, Receive, Send
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request
from src.backend.core.init_settings import global_settings


class DocProtectMiddleware:
    """Pure ASGI middleware to protect /docs, /redoc, /openapi.json behind login."""

    PROTECTED_PATHS = {"/docs", "/redoc", "/openapi.json"}

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"] in self.PROTECTED_PATHS:
            request = Request(scope)
            if not request.session.get("authenticated"):
                response = RedirectResponse(url="/login")
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


def setup_middleware(app) -> None:
    origins = [
        global_settings.API_BASE_URL,
        "http://localhost",
        "http://localhost:5000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(DocProtectMiddleware)
    app.add_middleware(
        SessionMiddleware,
        secret_key=global_settings.SECRET_KEY,
        max_age=1800,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
