from fastapi.responses import ORJSONResponse
from fastapi import status
import sentry_sdk


async def validation_exception_handler(request, err) -> ORJSONResponse:
    """
    Main exception handler for all routers,
    it returns if none of previous exceptions handlers catching anything
    """
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    sentry_sdk.capture_message(f"{base_error_message}. Detail: {err}")
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
