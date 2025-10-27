from datetime import datetime
from typing import Dict, List

from sqlalchemy import BOOLEAN, JSON, DateTime, ForeignKey, String, Text, func, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CommonModel(Base):
    __abstract__ = True
    
    db_status  : Mapped[str] = mapped_column(BOOLEAN, nullable=False, default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                            server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                  server_default=func.now(), onupdate=func.now())


class Langchain_User(CommonModel):
    __tablename__ = "langchain_user"
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    username : Mapped[str] = mapped_column(String(20), nullable=False)

    sessions : Mapped[List["Chat_Session"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan"
    )


class Chat_Session(CommonModel):
    __tablename__ = "chat_session"
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)

    user_id  : Mapped[int] = mapped_column(ForeignKey("langchain_user.id"), nullable=False)
    user : Mapped["Langchain_User"] = relationship(back_populates="sessions")
    
    title    : Mapped[str] = mapped_column(String(30), nullable=False)
    metadata : Mapped[Dict[str, str]] = mapped_column(JSON, nullable=False)

    messages : Mapped[List["Chat_Message"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan"    
    )


class Chat_Message(Base):
    __tablename__ = "chat_message"

    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)

    session_id : Mapped[int] = mapped_column(ForeignKey("chat_session.id"), nullable=False)
    session : Mapped["Chat_Session"] = relationship(back_populates="messages")
    
    role       : Mapped[str] = mapped_column(String(20), nullable=False)
    content    : Mapped[str] = mapped_column(Text, nullable=False)
    db_status  : Mapped[str] = mapped_column(BOOLEAN, nullable=False, default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                            server_default=func.now())