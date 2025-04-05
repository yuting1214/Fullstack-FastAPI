from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from backend.fastapi.core.init_settings import global_settings

def setup_cors(app):
    # Define the allowed origins
    origins = [
        global_settings.API_BASE_URL,
        "http://localhost",
        "http://localhost:5000",
    ]

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_session(app):
    # Add session middleware with a custom expiration time (e.g., 30 minutes)
    app.add_middleware(SessionMiddleware, 
                       secret_key="your_secret_key", 
                       max_age=1800)  # 1800 seconds = 30 minutes

async def doc_protect_middleware(request: Request, call_next):
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        if not request.session.get('authenticated'):
            return RedirectResponse(url="/login")
    response = await call_next(request)
    return response

def setup_doc_protect(app):
    app.middleware("http")(doc_protect_middleware)

def setup_gzip(app):
    app.add_middleware(GZipMiddleware, minimum_size=1000)

def setup_middleware(app):
    setup_cors(app)
    setup_doc_protect(app)
    setup_session(app)
    setup_gzip(app)