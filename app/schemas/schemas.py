from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal
from uuid import UUID


class OperationRequest(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal = Field(gt=0, description="Сумма должна быть больше 0")


class WalletOut(BaseModel):
    id: UUID
    balance: Decimal 

    class Config:
        from_attributes = True
