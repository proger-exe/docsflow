"""Main FastAPI app instance declaration."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse

from app.core.config import config
from app.api.api import api_router

app = FastAPI(
    title=config.project.NAME,
    version=config.project.VERSION,
    description=config.project.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/docs/",
    default_response_class=ORJSONResponse,
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.backend.CORS_ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(
    level=logging.INFO
)

# Guards against HTTP Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.backend.ALLOWED_HOSTS)