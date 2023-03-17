from schemas import UserLoginSchema
from core.config import JWTSettings
from fastapi import Depends, APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from service import UsersRepository


@AuthJWT.load_config
def get_config():
    return JWTSettings()


router = APIRouter()


# @router.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )


@router.post("/login")
async def login(user_login: UserLoginSchema, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)):
    user = await UsersRepository.get_user_by_email(session, user_login.email)
    #raise HTTPException(status_code=401, detail="Bad username or password")
    access_token = Authorize.create_access_token(
        subject=user.email, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}
