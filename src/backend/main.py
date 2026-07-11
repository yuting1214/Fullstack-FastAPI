import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.backend.core.config import global_settings
from src.backend.core.middleware import setup_middleware
from src.backend.core.lifespan import lifespan
from src.backend.core.routers import setup_routers

# JSON responses serialize through pydantic-core since FastAPI 0.130;
# ORJSONResponse is deprecated and orjson is no longer needed.
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/frontend/login/static"), name="static")

setup_middleware(app)
setup_routers(app)

if __name__ == "__main__":
    uvicorn.run(
        app="src.backend.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        reload=global_settings.ENV_MODE == "dev",
    )
