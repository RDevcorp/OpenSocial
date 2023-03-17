from database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
    __tablename__ = 'user'
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)  # password hash
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    status = Column(String, nullable=True)

    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
