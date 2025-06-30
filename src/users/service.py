from sqlalchemy import insert,select
from src.auth.utils import hash_password
from src.database.config import async_session
from src.users.models import UserOrm,VolunteerOrm,NeedyOrm

from  .schemas import UserAddSchema,VolunteerAddSchema,NeedyAddSchema

class UserService():

    @classmethod
    async def insert_user_from_db(cls,user: UserAddSchema):
        async with async_session() as session:
            query = insert(UserOrm).values(
                name= user.name,
                surname= user.surname,
                age= user.age,
                sex= user.sex,
                login= user.login,
                password_hash= hash_password(user.password_hash),
                role=user.role ,
                email=user.email ,
                phonenumber=user.phonenumber,
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def insert_volunteer_from_db(cls,volunteer: VolunteerAddSchema):
        async with async_session() as session:
            user_query = insert(UserOrm).values(
                name=volunteer.name,
                surname=volunteer.surname,
                age=volunteer.age,
                sex=volunteer.sex,
                login=volunteer.login,
                password_hash=hash_password(volunteer.password_hash),
                role=volunteer.role ,
                email=volunteer.email ,
                phonenumber=volunteer.phonenumber,
            )
            res = await session.execute(user_query)
            await session.commit()

            user_id = res.inserted_primary_key[0]
            volunteer_query = insert(VolunteerOrm).values(user_id = user_id,skills = volunteer.skills)
            await session.execute(volunteer_query)
            await session.commit()

    @classmethod
    async def insert_needy_from_db(cls,needy: NeedyAddSchema):
         async with async_session() as session:
            user_query = insert(UserOrm).values(
                name=needy.name,
                surname=needy.surname,
                age=needy.age,
                sex=needy.sex,
                login=needy.login,
                password_hash=hash_password(needy.password_hash),
                role=needy.role ,
                email=needy.email ,
                phonenumber=needy.phonenumber,
            )
            res = await session.execute(user_query)
            await session.commit()

            user_id = res.inserted_primary_key[0]
            needy_query = insert(NeedyOrm).values(user_id = user_id,address = needy.address)
            await session.execute(needy_query)
            await session.commit()


    
    @classmethod
    async def get_user_payload_by_login_from_db(cls,login: str):
        async with async_session() as session:
            query = select(UserOrm.login,UserOrm.password_hash,UserOrm.id,UserOrm.role).where(UserOrm.login == login)
            res = await session.execute(query)
            return res.first()
        
    @classmethod
    async def get_user_by_id_from_db(cls,id: int):
        async with async_session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            res = await session.execute(query)
            return res.scalar()
