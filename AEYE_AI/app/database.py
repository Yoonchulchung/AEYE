from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_postgres.vectorstores import PGVector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings

engine_mysql = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal_mysql = sessionmaker(autocommit=False, autoflush=False, bind=engine_mysql)
Base=declarative_base()


embedding_model = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-base")


vectorstore = PGVector(
    connection=settings.PG_CONN_STR,
    collection_name="pdf_chunks",
    embeddings=embedding_model,
)
