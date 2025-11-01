from psycopg2 import pool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import postgresql_db

db_url = (
    f"postgresql+psycopg2://{postgresql_db['user']}:{postgresql_db['password']}"
    f"@{postgresql_db['host']}:{postgresql_db['port']}/{postgresql_db['dbname']}"
)

try:
    engine = create_engine(db_url)
except Exception as e:
    print(f"Something wrong while creating engine: {e}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    connection_pool = pool.ThreadedConnectionPool(minconn=1, maxconn=10, **postgresql_db)
except Exception as e:
    print(f"Something wrong while creating connection pool : {e}")