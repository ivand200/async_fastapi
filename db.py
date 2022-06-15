from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from databases import Database
from settings import Settings

settings = Settings()


DATABASE_URL = f"sqlite:///./{settings.database_url}"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

def get_database() -> Database:
    return database
