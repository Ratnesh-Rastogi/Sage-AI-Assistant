"""
Application entry point.

SAGE_BLUEPRINT.md Section 88:
Responsibilities: create the FastAPI app, load configuration, initialize the
database, register routes/middleware, start background services.
It must NOT contain business logic.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import chat, health
from app.config.settings import get_settings
from app.core.exceptions import BaseApplicationException
from app.logging.logger import configure_logging, get_logger
from app.tools.bootstrap import bootstrap_tools

settings = get_settings()

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s in %s mode", settings.APP_NAME, settings.APP_ENV)
    bootstrap_tools()
    # Phase 3+ will start the scheduler / background workers here.
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sage API",
        description="Private, self-hosted personal AI assistant.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        response = await call_next(request)
        logger.info(
            "%s %s -> %s", request.method, request.url.path, response.status_code
        )
        return response

    @app.exception_handler(BaseApplicationException)
    async def application_exception_handler(request: Request, exc: BaseApplicationException):
        logger.error("Application error on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=400, content=exc.to_dict())

    app.include_router(health.router, prefix=settings.API_V1_PREFIX)
    app.include_router(chat.router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
