#!/usr/bin/env python3
"""
Defines a module with SQLAlchemy model named User for a database table
named users
"""
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__: str = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250))
    reset_token: Optional[str] = Column(String(250))
