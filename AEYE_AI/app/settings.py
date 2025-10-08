import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    SQLALCHEMY_DATABASE_URL=os.getenv("SQLALCHEMY_DATABASE_URL")
    PG_CONN_STR=os.getenv("PG_CONN_STR")
    PG_CON=os.getenv("PG_CON")
    

settings = Settings()