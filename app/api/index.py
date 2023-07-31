from fastapi import APIRouter

from app.api import admins
from app.api import auth
from app.api import users

router = APIRouter(prefix="/api")

router.include_router(admins.router)
router.include_router(auth.router)
router.include_router(users.router)


@router.get("/")
async def root():
    return {"message": "Hello from api!"}

