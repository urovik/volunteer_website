from fastapi import HTTPException,status
from typing import List
from .models import RequestOrm
from .schemas import AddRequestSchema,RequestSchema

from sqlalchemy import insert,update,select
from src.database.config import async_session


class RequestService():

    @classmethod
    async def get_all_request_from_db(cls) -> RequestOrm:
        async with async_session() as session:
            query = select(RequestOrm)
            res = await session.execute(query)
            return res.scalars().all()
        
    @classmethod
    async def get_accepted_request_volunteer_from_db(cls,volunteer_id: int) -> List[RequestOrm]:
        async with async_session() as session:
            query = select(RequestOrm).where(RequestOrm.volunteer_id == volunteer_id)
            res = await session.execute(query)
            return res.scalars().all()        
    
    @classmethod
    async def insert_request_from_db(cls,needy_id,request: AddRequestSchema):
        async with async_session() as session:
            query = insert(RequestOrm).values(
                needy_id = needy_id,
                location = request.location,
                description = request.description,
            )
            await session.execute(query)
            await session.commit()

    @classmethod 
    async def update_volunteer_id_from_request(cls,request_id: int,volunteer_id: int):
        async with async_session() as session:
            request_query = select(RequestOrm).where(RequestOrm.id == request_id)
            result = await session.execute(request_query)
            request = result.scalar_one_or_none()  # получаем объект заявки или None, если не найдена

        # Проверка, найдена ли заявка
            if request is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="заявка не найдена"
                )

            query = update(RequestOrm).where(RequestOrm.id==request_id).values(
                volunteer_id=volunteer_id
            )
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def get_created_request_needy_from_db(cls,needy_id: int) -> List[RequestOrm]:
        async with async_session() as session:
            query = select(RequestOrm).where(RequestOrm.needy_id == needy_id)
            res = await session.execute(query)
            return res.scalars().all() 

            