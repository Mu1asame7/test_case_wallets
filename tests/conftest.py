import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import engine, Base
from sqlalchemy import text


@pytest.fixture(scope="function")
async def client():
    """Максимально простой клиент"""

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем клиент
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # Очищаем таблицы после теста
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM payments;"))
        await conn.execute(text("DELETE FROM wallets;"))
        await conn.commit()
