from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from databases import Database

DATABASE_URL = "sqlite:///./fake.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database_test = Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

def get_test_database() -> Database:
    return database_test
