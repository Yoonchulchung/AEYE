
from sqlalchemy import INTEGER, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Result(Base):
    __tablename__ = "Result"
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    classification: Mapped[str] = mapped_column(String(64), nullable=False)
    result: Mapped[str] = mapped_column(String(2048), nullable=False)
    result_summary: Mapped[str] = mapped_column(String(2048), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)