import asyncio
import socket

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from starlette import status

from api.docs import health_response
from dependencies import SessionDep

health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@health_router.get(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=health_response,
)
async def health(session: SessionDep) -> None:
    """
    Checks whether db is alive, and backend is working
    """
    try:
        await asyncio.wait_for(session.execute(text("SELECT 1;")), timeout=30)
    except (
        asyncio.TimeoutError,
        socket.gaierror,
        Exception,
    ):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return None
