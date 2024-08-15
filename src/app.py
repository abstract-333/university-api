from typing import Final

import sentry_sdk
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis
from sqladmin import Admin

from admin import AdminAuth
from exception.handler import validation_exception_handler
from settings import settings_obj
from storage.database.config import AsyncSessionFactory
from storage.redis.config import RedisConnectionFactory
from views_routers import routers, views

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


def app_factory() -> FastAPI:
    sentry_sdk.init(
        dsn=settings_obj.SENTRY_URL,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        # On startup
        redis: Final[Redis] = await RedisConnectionFactory().get_instance()
        FastAPICache.init(backend=RedisBackend(redis=redis), prefix="fastapi-cache")

        yield
        # On shutdown
        await FastAPICache.clear()
        client = sentry_sdk.Hub.current.client
        if client is not None:
            client.close(timeout=2.0)

    def register_static_docs_routes(app: FastAPI):
        @app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html() -> HTMLResponse:
            return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
                swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect() -> HTMLResponse:
            return get_swagger_ui_oauth2_redirect_html()

        @app.get("/redoc", include_in_schema=False)
        async def redoc_html() -> HTMLResponse:
            return get_redoc_html(
                openapi_url=app.openapi_url,
                title=app.title + " - ReDoc",
                redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
            )

    fastapi_app = FastAPI(
        title="Tishreen University",
        version="0.0.2",
        lifespan=app_lifespan,
        exception_handlers={Exception: validation_exception_handler},
        docs_url=None,
        redoc_url=None,
        default_response_class=ORJSONResponse,
    )

    fastapi_app.add_middleware(
        middleware_class=BrotliMiddleware,
        quality=6,
        minimum_size=1000,
    )
    authentication_backend = AdminAuth(secret_key=settings_obj.JWT_SECRET_KEY)

    admin = Admin(
        app=fastapi_app,
        authentication_backend=authentication_backend,
        engine=AsyncSessionFactory().get_async_engine(),
        session_maker=AsyncSessionFactory().get_async_session_maker(),
        title="Tishreen University",
    )

    for view in views:
        admin.add_view(view=view)

    register_static_docs_routes(app=fastapi_app)
    for router in routers:
        fastapi_app.include_router(router=router)

    return fastapi_app


app: FastAPI = app_factory()
