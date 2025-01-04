from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "sqlite:////home/site/wwwroot/sqlite.db"
# DATABASE_URL = "sqlite:////home/site/wwwroot/sqlite_t1.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", String, unique=True, index=True),
    Column("username", String, unique=False, index=True),
    Column("email", String, unique=True, index=True),
    Column("phone", String, unique=True, index=True),
)

issues = Table(
    "issues",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("issue", String),
    Column("location", String),
    Column("phone", Integer),
    Column("complaintid", String, unique=True, index=True),
    Column("esttime", String),
    Column("opentime", String),
	Column("closetime", String),
    Column("name", String),
    Column("user_id", String),
    Column("status", String),
    Column("payments_receipt", String),
)

service_engineers = Table(
    "service_engineers",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("engineer_id", String, unique=True, index=True),
    Column("name", String),
    Column("phone", Integer, unique=True, index=True),
    Column("availability", Boolean),
)

otp = Table(
    "otp",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", String, unique=True, index=True),
    Column("otp", Integer),
    Column("UTC", String),
)


metadata.create_all(bind=engine)