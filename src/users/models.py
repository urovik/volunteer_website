import datetime

from sqlalchemy import func,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy.types import Enum,Integer,Date,Time,Text

from src.database.base import Base
from enum import Enum as PyEnum


class Roles(PyEnum):
    ADMIN = 'админ'
    NEEDY = 'нуждающийся'
    VOLUNTEER = 'волонтер'

class Gender(PyEnum):
    MALE = 'мужск'
    FEMALE = 'женск'


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[Gender] = mapped_column(Enum(Gender))
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes] = mapped_column(nullable=True)
    role: Mapped[Roles] = mapped_column(Enum(Roles))
    email: Mapped[str] = mapped_column(unique=True)
    phonenumber: Mapped[str] = mapped_column(unique=True)
    registration_date: Mapped[datetime.date] = mapped_column(Date, default=func.current_date())
    registration_time: Mapped[datetime.time] = mapped_column(Time, default=func.current_time())


class VolunteerOrm(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(column= "users.id"),unique=True)
    skills: Mapped[str] = mapped_column(Text)


class NeedyOrm(Base):
    __tablename__ = "needys"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(column= "users.id"),unique=True)
    address: Mapped[str]
    