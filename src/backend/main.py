import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from src.backend.core.init_settings import args
from src.backend.core.middleware import setup_middleware
from src.backend.core.lifespan import lifespan
from src.backend.core.routers import setup_routers

app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

app.mount("/static", StaticFiles(directory="src/frontend/login/static"), name="static")

setup_middleware(app)
setup_routers(app)

if __name__ == "__main__":
    uvicorn.run(
        app="src.backend.main:app",
        host=args.host,
        port=int(os.getenv("PORT", "5000")),
        reload=args.mode == "dev",
    )
