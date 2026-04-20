from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import AsyncSession, get_db
from sqlalchemy import select
from uuid import UUID
from app.schemas.schemas import OperationRequest, WalletOut
from app.models.models import Wallet, Payment


router = APIRouter(tags=["wallets"])


@router.post("/", response_model=WalletOut, status_code=status.HTTP_201_CREATED)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    """Создать новый кошелёк с нулевым балансом"""
    new_wallet = Wallet(balance=0)
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    return new_wallet


@router.get("/{wallet_uuid}", response_model=WalletOut)
async def get_wallet(wallet_uuid: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wallet).where(Wallet.id == wallet_uuid))

    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
        )

    return wallet


@router.post("/{wallet_uuid}/operation", response_model=WalletOut)
async def operate_wallet(
    wallet_uuid: UUID, operation: OperationRequest, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
    )

    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
        )

    if operation.operation_type == "DEPOSIT":
        wallet.balance += operation.amount
    elif operation.operation_type == "WITHDRAW":
        if wallet.balance >= operation.amount:
            wallet.balance -= operation.amount
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
            )

    new_payment = Payment(
        operation_type=operation.operation_type,
        amount=operation.amount,
        wallet_id=wallet_uuid,
    )

    db.add(new_payment)
    await db.commit()
    await db.refresh(wallet)

    return wallet
