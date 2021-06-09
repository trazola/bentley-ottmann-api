from typing import AsyncGenerator

from bentley_ottmann_api.conf import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_uri, pool_pre_ping=True)
MainSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncGenerator:
    """
    Dependence creates new session for db.

    Returns:
        new db session
    """
    db = MainSession()
    try:
        yield db
    finally:
        db.close()
