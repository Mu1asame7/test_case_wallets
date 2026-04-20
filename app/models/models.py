import uuid
from sqlalchemy import (
    Integer,
    String,
    Column,
    DECIMAL,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(DECIMAL(10, 2), default=0)

    __table_args__ = (CheckConstraint("balance >=0", name="check_balannce"),)

    payments = relationship(
        "Payment", back_populates="wallet", cascade="all, delete-orphan"
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    wallet_id = Column(
        UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False
    )
    wallet = relationship("Wallet", back_populates="payments")
