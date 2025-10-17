
from database import Base
from sqlalchemy import DateTime, String, INTEGER
from sqlalchemy.orm import Mapped, mapped_column


class Result(Base):
    __tablename__ = "Result"
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(INTEGER, nullable=False, unique=True)
    result: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    
    
class Image(Base):
    __tablename__ = "Result"

    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    img_path: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)