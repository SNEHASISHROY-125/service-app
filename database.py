from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("password", String),
)

issues = Table(
    "issues",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("issue", String),
    Column("location", String),
    Column("phone", Integer),
    Column("complaintid", Integer),
    Column("esttime", String),
    Column("name", String),
)

metadata.create_all(bind=engine)