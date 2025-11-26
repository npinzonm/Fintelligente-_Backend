from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "auth_users"

    id = Column(String(36), primary_key=True)
    name = Column(String(150))
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
