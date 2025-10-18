
from sqlalchemy import INTEGER, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class InferenceResult(Base):
    __tablename__ = "InferenceResult"
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    result: Mapped[str] = mapped_column(String(2048), nullable=False)
    classification: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    
    
class Image(Base):
    __tablename__ = "Image"

    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    img_path: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)