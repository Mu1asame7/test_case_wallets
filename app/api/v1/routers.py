from fastapi import APIRouter
from app.api.v1.endpoints import wallets

router = APIRouter()

router.include_router(wallets.router, prefix="/wallets", tags=["wallets"])