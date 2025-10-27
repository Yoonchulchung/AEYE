from datetime import datetime
from typing import List

from sqlalchemy import BOOLEAN, DATETIME, JSON, ForeignKey, Integer, String, Text, func, \
                       INTEGER
from pgvector.sqlalchemy import VECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CommonModel(Base):
    __abstract__ = True
    
    db_status  : Mapped[str] = mapped_column(BOOLEAN, nullable=False, default=True)
    created_at : Mapped[str] = mapped_column(DATETIME, nullable=False, 
                                             server_default=func.now())
    

class Paper(CommonModel):
    __tablename__ = 'paper'
    
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    title     : Mapped[str] = mapped_column(Text, nullable=False)
    authors   : Mapped[List[str]] = mapped_column(JSON, nullable=False) 
    published : Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    abstract  : Mapped[str] = mapped_column(Text, nullable=False)
    language  : Mapped[str] = mapped_column(String(10), nullable=False)
    keywords  : Mapped[List[str]] = mapped_column(JSON, nullable=False)
    category  : Mapped[List[str]] = mapped_column(JSON, nullable=False)
    
    chunks: Mapped[List["PaperChunk"]] = relationship(
        back_populates="paper",
        cascade="all, delete-orphan"
    )
    

class PaperChunk(CommonModel):
    __tablename__ = 'paper_chunk'

    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)

    paper_id      : Mapped[int] = mapped_column(ForeignKey("paper.id"), nullable=False)
    paper: Mapped["Paper"] = relationship(back_populates="chunks")
    
    chunk_index   : Mapped[int] = mapped_column(Integer, nullable=False)
    section_title : Mapped[str] = mapped_column(String, nullable=False)
    char_start    : Mapped[int] = mapped_column(Integer, nullable=False)
    char_end      : Mapped[int] = mapped_column(Integer, nullable=False)
    content       : Mapped[str] = mapped_column(Text, nullable=False)
    embedding     : Mapped[List[float]] = mapped_column(VECTOR(dim=768), nullable=False)