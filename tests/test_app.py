from pathlib import Path
import sys
import httpx
import pytest

sys.path.append(str(Path(__file__).parent.parent))
from src.settings.settings import settings_obj_test


@pytest.mark.parametrize(
    "router, status_code, result",
    [
        ("/health", 204, ""),
        ("/health", 204, ""),
    ],
)
@pytest.mark.asyncio
async def test_health(
    client: httpx.AsyncClient,
    router: str,
    status_code: int,
    result: str,
) -> None:
    print(settings_obj_test.DB_NAME)
    response = await client.get(router)
    assert response.status_code, response.text == (status_code, result)
