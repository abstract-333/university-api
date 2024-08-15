from typing import AsyncIterator

import httpx
import pytest_asyncio


@pytest_asyncio.fixture(scope="session", autouse=True)
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client


# @pytest.fixture(scope="session", autouse=True)
# def setup_db() -> None:
#     print(f"{settings_obj.DB_NAME=}")
#     assert settings_obj.MODE == "TEST"
#     BaseModelORM.metadata.drop_all(UOWDep.session)
#     BaseModelORM.metadata.create_all(async_engine)
