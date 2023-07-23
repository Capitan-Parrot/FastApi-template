from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["user"])


# @router.get("/getUsers", response_model=schemas.User)
# async def login(login_request: schemas.LoginUserRequest, db: Session = Depends(get_db)):
#     user = authenticate_user(db, login_request)
#     if not user:
#         raise HTTPException(status_code=400, detail="Почта или пароль некорректны")
#     return user

