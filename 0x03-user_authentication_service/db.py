#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
from typing import Any


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create user and store in database"""

        # Create a user instance
        user = User(email=email, hashed_password=hashed_password)

        # Store user to db
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Any) -> User:
        """Searches for user based on its attributes"""
        user = self._session.query(User).filter_by(**kwargs).one()
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """Updates a specified user attributes"""
        # Raise a ValueError if argument not in user attributes
        valid_columns = User.__table__.columns.keys()
        for key in kwargs:
            if key not in valid_columns:
                raise ValueError  # raise an exception

        # Update user record
        self._session.query(User).filter_by(id=user_id).update(kwargs)

        # Commit changes to db
        self._session.commit()
