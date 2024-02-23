#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Mapping, Union, Dict
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """add user to database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row foun in the users table"""
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in ['id', 'email', 'hashed_password',
                           'session_id', 'reset_token']:
                raise InvalidRequestError
        data = self._session.query(User).filter_by(**kwargs).first()
        if data is None:
            raise NoResultFound
        elif self._session.query(User).filter_by(**kwargs).count() > 1:
            raise InvalidRequestError
        return data

    def update_user(self, user_id: int, **kwargs) -> None:
        """update users info"""
        if not kwargs:
            return None
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in ['id', 'email', 'hashed_password',
                           'session_id', 'reset_token']:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None
