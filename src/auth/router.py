from fastapi import APIRouter


from fastapi import APIRouter,Depends,Response

from src.users.models import UserOrm,Roles
from src.users.schemas import UserPayloadSchema
import src.auth.utils as auth_utils
from .dependencies import validate_auth_user,get_current_auth_user,required_roles
from .schemas import TokenInfo

auth_router = APIRouter(prefix="/auth/jwt",tags=['аунтефикация и авторизация'])



@auth_router.post('/token')
async def login(response: Response,user: UserPayloadSchema = Depends(validate_auth_user)) -> TokenInfo:
    jwt_payload = {
        "sub": str(user.id),
        "login": user.login,
        "role": str(user.role)    
    }
    token = auth_utils.encode_jwt(jwt_payload)
     #Устанавливаем токен в куку
    response.set_cookie(
        key="access_token",
        value=token,
        samesite='strict',
        httponly= True,
    )
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )

@auth_router.get("/profile")
async def auth_user_profile(
    user: UserOrm = Depends(get_current_auth_user)
):
    return {
        "login": user.login,
        "id": user.id,
        "role": user.role
    }


@auth_router.get("/data")
@required_roles([Roles.ADMIN])
async def get_important_data(
    user: UserOrm = Depends(get_current_auth_user)
):
    return "hello admin"
 
@auth_router.post("/logout")    
async def logout(
    response: Response
):
    response.delete_cookie(
        key="access_token",
        samesite='strict',
        httponly= True,
    )
    return {"msg":"Вы успешно вышли из аккаунта"}