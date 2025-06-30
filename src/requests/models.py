import datetime

from src.database.base import Base

from sqlalchemy import ForeignKey,func
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy.types import Text,Enum,Date,Time

from enum import Enum as PyEnum

class Status(PyEnum):
    COMPLETED = "Выполнена"
    IN_PROGRESS = "В процессе"
    FREE = "свободная"

class RequestOrm(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    needy_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"),nullable=False)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"),nullable=True)
    location: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status),default=Status.FREE)
    data_created: Mapped[datetime.date] = mapped_column(Date, default=func.current_date())
    time_created: Mapped[datetime.time] = mapped_column(Time, default=func.current_time())
    data_completed: Mapped[datetime.date] = mapped_column(Date,nullable=True)
    time_completed: Mapped[datetime.time] = mapped_column(Time,nullable=True)