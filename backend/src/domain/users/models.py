from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db import Base


class Users(Base):
    __tablename__ = "users"
  
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = Mapped(String(50), null=True)
    surname: Mapped[str] = Mapped(String(50), null=True)
    last_name: Mapped[str] = Mapped(String(50), null=True)
    hashed_password: Mapped[str] = mapped_column(String(128))