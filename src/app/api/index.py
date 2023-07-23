from fastapi import APIRouter

from app.api import users

router = APIRouter(prefix="/api")
router.include_router(users.router)


@router.get("/")
async def root():
    return {"message": "Hello"}

