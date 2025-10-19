from sqlalchemy import INTEGER, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
class Request(Base):
    __tablename__ = "Request"

    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    img_path: Mapped[str] = mapped_column(String(64), nullable=False)
    job_id: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)