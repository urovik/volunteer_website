from fastapi import APIRouter,Depends

from .schemas import AddRequestSchema,RequestSchema
from src.users.models import UserOrm,Roles
from src.auth.dependencies import get_current_auth_user,required_roles

from .service import RequestService

request_router = APIRouter(prefix="/api/requests",tags=['заявки'])


@request_router.post("")
@required_roles([Roles.NEEDY])
async def create_request(request: AddRequestSchema,user: UserOrm = Depends(get_current_auth_user)):
    await RequestService.insert_request_from_db(needy_id=user.id,request=request)
    return {"msg": "Заявка успешно создана"}

@request_router.put("/{request_id}")
@required_roles([Roles.VOLUNTEER])
async def accept_request(request_id: int,user: UserOrm = Depends(get_current_auth_user)):
    await RequestService.update_volunteer_id_from_request(request_id=request_id,volunteer_id=user.id)
    return {"msg": f"волонтер c id: {user.id} успешно взял заявку"}

@request_router.get("")
@required_roles([Roles.ADMIN,Roles.VOLUNTEER])
async def get_all_requests(user: UserOrm = Depends(get_current_auth_user)):
    return await RequestService.get_all_request_from_db()

@request_router.get("/volunteer")
@required_roles([Roles.VOLUNTEER])
async def get_accepted_request_volunteer(user: UserOrm = Depends(get_current_auth_user)):
    return await RequestService.get_accepted_request_volunteer_from_db(volunteer_id=user.id)

@request_router.get("/needy")
@required_roles([Roles.NEEDY])
async def get_created_requests_needy(user: UserOrm = Depends(get_current_auth_user)):
    return await RequestService.get_created_request_needy_from_db(needy_id=user.id)