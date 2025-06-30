from pydantic import BaseModel, EmailStr,Field

from .models import Roles,Gender


class UserAddSchema(BaseModel):
    name: str
    surname: str
    age: int
    sex: Gender
    login: str
    password_hash: str
    role: Roles
    email: EmailStr
    phonenumber: str

class VolunteerAddSchema(UserAddSchema):
    role: Roles = Roles.VOLUNTEER
    skills: str

class NeedyAddSchema(UserAddSchema):
    role: Roles = Roles.NEEDY
    address: str
    


class UserPayloadSchema(BaseModel):
    id: int
    login: str
    role: Roles