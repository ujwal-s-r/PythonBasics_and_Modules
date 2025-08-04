# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Make sure to use your actual Postgres user, password, host, and db name
# The format is: "postgresql+asyncpg://USER:PASSWORD@HOST/DATABASE"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:ujwal@localhost/fastapidb"

# The engine is the core interface to the database
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# The sessionmaker provides a factory for creating sessions
# An AsyncSession is the handle for our database operations
async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

# This Base will be used by our models
class Base(DeclarativeBase):
    pass