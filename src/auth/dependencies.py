from fastapi import Cookie, Depends, Form, HTTPException, status
from jwt import DecodeError


from src.users.schemas import UserPayloadSchema
from src.users.models import UserOrm
from src.users.service import UserService
import src.auth.utils as auth_utils

from typing import Callable
from functools import wraps

async def validate_auth_user(
    login: str = Form(),
    password: str = Form()
) -> UserPayloadSchema:
    unauthed_exp = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="invalid password or name")
    
    if not (user:= await UserService.get_user_payload_by_login_from_db(login)):
        raise unauthed_exp
    
    if not auth_utils.validate_password(
        password=password,
        hash_password=user.password_hash
    ):
        raise unauthed_exp
    return user


async def get_current_token_payload_user(
    access_token: str = Cookie(None)
) -> UserPayloadSchema:
    try:
        token = access_token
        if access_token is None:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="token missing"
            )
        payload = auth_utils.decode_jwt(
        token=token,
    )
        return payload
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid"
        )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload_user)
) -> UserOrm:
    id: int = int(payload.get("sub"))
    if not (user := await UserService.get_user_by_id_from_db(id=id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not found"
        )
    return user


# декоратор для проверки роли 
def required_roles(roles: list):
    def wrapper(func: Callable):
        @wraps(func)
        async def validate_role(*args,user: UserOrm,**kwargs):
            if user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно прав"
                )
            return await func(*args,user=user,**kwargs)
        return validate_role
    return wrapper