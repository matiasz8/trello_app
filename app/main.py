import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import (APP_NAME, APP_VERSION, IS_DEBUG)


app_config = {'title': APP_NAME,
              'version': APP_VERSION,
              'debug': IS_DEBUG,
              'openapi_url': '/openapi.json' if bool(IS_DEBUG) else None}


def start_app() -> FastAPI:
    fast_app = FastAPI(**app_config)
    fast_app.include_router(api_router)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fast_app


app = start_app()

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
