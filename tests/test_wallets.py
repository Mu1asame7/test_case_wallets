import pytest
from uuid import UUID
import asyncio

pytestmark = pytest.mark.asyncio


async def test_wallet_operations(client):
    """Все тесты в одном сценарии"""

    # 1. Тест создания кошелька
    create_response = await client.post("/api/v1/wallets/")
    assert create_response.status_code == 201
    wallet_data = create_response.json()
    wallet_id = wallet_data["id"]
    assert float(wallet_data["balance"]) == 0
    assert UUID(wallet_id)

    # 2. Тест получения кошелька
    get_response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert float(data["balance"]) == 0
    assert data["id"] == wallet_id

    # 3. Тест получения несуществующего кошелька
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    not_found_response = await client.get(f"/api/v1/wallets/{fake_uuid}")
    assert not_found_response.status_code == 404
    assert not_found_response.json()["detail"] == "Wallet not found"

    # 4. Тест пополнения
    deposit_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 100.50},
    )
    assert deposit_response.status_code == 200
    assert float(deposit_response.json()["balance"]) == 100.50

    # 5. Тест списания
    withdraw_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 50.00},
    )
    assert withdraw_response.status_code == 200
    assert float(withdraw_response.json()["balance"]) == 50.50

    # 6. Тест списания при недостатке средств
    insufficient_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 1000},
    )
    assert insufficient_response.status_code == 400
    assert insufficient_response.json()["detail"] == "Insufficient funds"
