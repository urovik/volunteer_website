from  fastapi import APIRouter,Depends
from src.users.schemas import UserAddSchema,VolunteerAddSchema,NeedyAddSchema
from src.users.service import UserService

from src.auth.dependencies import required_roles,get_current_auth_user
from .models import Roles,UserOrm

user_router = APIRouter(prefix="/api/users",tags=['пользователи'])


@user_router.post("")
@required_roles([Roles.ADMIN])
async def insert_user(insert_user: UserAddSchema,user: UserOrm = Depends(get_current_auth_user)):
    await UserService.insert_user_from_db(insert_user)
    return {'msg': f"пользователь {insert_user.name} добавлен в базу "}

@user_router.post("/volunteers")
async def register_volunteer(volunteer: VolunteerAddSchema):
    await UserService.insert_volunteer_from_db(volunteer)
    return {"msg": f"волонтер с именем {volunteer.name} добавлен"}

@user_router.post("/needys")
async def register_needy(needy: NeedyAddSchema):
    await UserService.insert_needy_from_db(needy)
    return {"msg": f"Нуждающийся успешно добавлен"}